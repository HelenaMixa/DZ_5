from django.db import models


class Coach(models.Model):
    coach_surname = models.CharField(max_length=100)
    coach_name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    mail = models.EmailField(db_index=True)

    def __str__(self):
        return f"{self.coach_surname}" \
               f"{self.coach_name}" \
               f"{self.telephone}{self.mail}"


class Club(models.Model):
    club_name = models.CharField(max_length=100)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, null=True)
    city = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.club_name}" \
               f"{self.coach}" \
               f"{self.city}"


class Dancer(models.Model):
    dancer_surname = models.CharField(max_length=50)
    dancer_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, null=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.dancer_surname}" \
               f"{self.dancer_name}" \
               f"{self.birth_date}" \
               f"{self.coach}{self.club}"

