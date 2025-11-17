class Employee:
    def __init__(self, name, _id, salary):
        self.name = name
        self.id = _id
        self.salary = salary

    def cal_salary(self):
        return self.salary
    
    def display_info(self):
        print(f"员工的姓名是：{self.name}, 员工号是{self._id}, 基本工资是{self.cal_salary()}")

class Manager(Employee):
    def __init__(self, name, _id, salary, jintie):
        super().__init__(name, _id, salary)
        self.jintie = jintie

    def cal_salary(self):
        return self.salary + self.jintie
    
    def display_info(self):
        super().display_info()
        print(f"职位是经理，管理津贴是{self.jintie}, 总工资是{self.cal_salary()}")

        

if __name__ == '__main__':
    emp1 = Employee( name : "张三", _id:"01", salary:2000)
    emp1.display_info()

    print('*' * 20)
    emp2 = Manager()
