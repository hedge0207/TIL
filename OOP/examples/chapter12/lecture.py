from typing import List


class Lecture:

    def __init__(self, title: str, pass_: int, scores: List[int]):
        self._title = title
        self._pass = pass_
        self._scores = scores

    def average(self):
        return sum(self._scores) / len(self._scores) if self._scores else 0
    
    def evaluate(self):
        return "Pass:{} Faile:{}".format(self._pass_count(), self._fail_count())
    
    def _pass_count(self):
        return len([score for score in self._scores if score >= self._pass])
    
    def _fail_count(self):
        return len([score for score in self._scores if score < self._pass])
    
    def stats(self):
        return f"Title: {self._title} Evaluation Method: {self._get_evaluation_method()}"
    
    def _get_evaluation_method(self):
        return "Pass or Fail"

    @property
    def score(self):
        return self._scores
    

class Grade:

    def __init__(self, name: str, upper: int, lower: int):
        self._name = name
        self._upper = upper
        self._lower = lower

    def is_name(self, name: str):
        return self._name == name
    
    def include(self, score: int):
        return self._lower <= score <= self._upper

    @property
    def name(self):
        return self._name


class GradeLecture(Lecture):

    def __init__(self, name: str, pass_: int, grades: List[Grade], scores: List[int]):
        super().__init__(name, pass_, scores)
        self._grades = grades

    def evalutate(self):
        return super().evaluate() + ", " + self._grade_statistics()

    def _grade_statistics(self):
        return " ".join(["{}:{}".format(grade.name, self._grade_count(grade)) for grade in self._grades])
    
    def _grade_count(self, grade: Grade):
        return len([score for score in self._scores if grade.include(score)])

    def _get_evaluation_method(self):
        return "Grade"
    

class FormattedGradeLecture(GradeLecture):

    def format_average(self):
        return f"Avg: {super().average()}"


class Professor:

    def __init__(self, name, lecture: Lecture):
        self._lecture_name = name
        self._lecture = lecture
    
    def compile_statistics(self):
        return f"[{self._lecture_name}] {self._lecture.evaluate()} - Avg: {self._lecture.average()}"

if __name__ == "__main__":

    # propessor = Professor("DFS", Lecture("Algorithm", 
    #                                         80, 
    #                                         [75, 80, 95, 60, 85]))
    
    # propessor = Professor("DFS", GradeLecture("Algorithm", 
    #                                         80, 
    #                                         [
    #                                             Grade("A", 100, 95), 
    #                                             Grade("B", 94, 80), 
    #                                             Grade("C", 79, 70), 
    #                                             Grade("D", 69, 50), 
    #                                             Grade("F", 49, 0)
    #                                         ],
    #                                         [75, 80, 95, 60, 85]))
    # print(propessor.compile_statistics())

    lecture = FormattedGradeLecture("Algorithm", 
                            80, 
                            [
                                Grade("A", 100, 95), 
                                Grade("B", 94, 80), 
                                Grade("C", 79, 70), 
                                Grade("D", 69, 50), 
                                Grade("F", 49, 0)
                            ],
                            [75, 80, 95, 60, 85])
    print(lecture.format_average())