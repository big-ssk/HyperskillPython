from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, date, timedelta

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=date.today())

    def __repr__(self):
        return self.task


class Interface:

    def __init__(self):
        self.today = date.today()
        self.tasks = None
        self.engine = create_engine('sqlite:///todo.db?check_same_thread=False')
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()
        self.actions = {'1': self.get_tasks_for_today,
                        '2': self.get_tasks_for_week,
                        '3': self.get_all_tasks,
                        '4': self.get_missed_tasks,
                        '5': self.add_task,
                        '6': self.delete_task,
                        '0': self.exit}

    def show_menu(self):
        print("1) Today's tasks",
              "2) Week's tasks",
              "3) All tasks",
              "4) Missed tasks",
              "5) Add task",
              "6) Delete task",
              "0) Exit", sep='\n')

    def print_tasks(self, with_date=True):
        if with_date:
            for num, task in self.tasks:
                print(f"{num}. {task}. {date.strftime(task.deadline, '%-d %b')}")
        else:
            if self.tasks:
                for num, task in self.tasks:
                    print(f'{num}. {task}')
            else:
                print('Nothing to do!')

    def add_task(self):
        new_task = input("\nEnter task\n")
        tasks_deadline = input("Enter deadline\n")
        tasks_deadline = datetime.strptime(tasks_deadline, '%Y-%m-%d').date()
        self.session.add(Table(task=new_task, deadline=tasks_deadline))
        self.session.commit()
        print("The task has been added!")

    def delete_task(self):
        self.tasks = list(enumerate(self.session.query(Table).order_by(Table.deadline).all(), 1))
        if not self.tasks:
            print("Nothing to delete")
        else:
            print("\nChoose the number of the task you want to delete:")
            self.print_tasks()
            num_to_delete = int(input())
            _, task_to_delete = list(*filter(lambda task: task[0] == num_to_delete, self.tasks))
            self.session.delete(task_to_delete)
            self.session.commit()
            print("The task has been deleted!")

    def get_missed_tasks(self):
        self.tasks = list(enumerate(self.session.query(Table).filter(Table.deadline < self.today), 1))
        print("\nMissed tasks:")
        if not self.tasks:
            print("Nothing is missed")
        else:
            self.print_tasks()

    def get_tasks_for_week(self):
        tasks = self.session.query(Table).filter(Table.deadline.between(self.today, self.today + timedelta(days=7)))
        for i in range(7):
            day = date.today() + timedelta(days=i)
            print('\n' + date.strftime(day, '%A %-d %b:'))
            self.tasks = list(enumerate(filter(lambda task: day == task.deadline, tasks), 1))
            self.print_tasks(with_date=False)

    def get_all_tasks(self):
        self.tasks = list(enumerate(self.session.query(Table).order_by(Table.deadline).all(), 1))
        print("\nAll tasks:")
        self.print_tasks()

    def get_tasks_for_today(self):
        self.tasks = list(enumerate(self.session.query(Table).filter(Table.deadline == self.today), 1))
        print(f'\nToday {date.strftime(self.today, "%-d %b")}:')
        self.print_tasks(with_date=False)

    def exit(self):
        exit('Bye!')

    def main(self):
        while True:
            self.show_menu()
            action = input()
            self.actions.get(action)()
            print()


interface = Interface()
interface.main()
