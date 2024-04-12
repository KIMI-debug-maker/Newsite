from django.db import models

# Create your models here.


class User(models.Model):
    UserID = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    Identity = models.CharField(max_length=32, default='basic')

    def __str__(self):
        return self.Username


class Now_cast_data(models.Model):
    Time = models.DateTimeField()
    growth = models.DecimalField(max_digits=20, decimal_places=10)
    Economy = models.DecimalField(max_digits=20, decimal_places=10)
    Mood = models.DecimalField(max_digits=20, decimal_places=10)
    Price = models.DecimalField(max_digits=20, decimal_places=10)
    Finance = models.DecimalField(max_digits=20, decimal_places=10)


# class UserInfo(models.Model):
#     UserID = models.ForeignKey(User, on_delete=models.CASCADE)
#     Institute = models.CharField(max_length=200)
#     Title = models.CharField(max_length=200)
#     Country = models.CharField(max_length=200)
#
#
# class Focus(models.Model):
#     UserID = models.ForeignKey(User, on_delete=models.CASCADE)
#     stocks = models.CharField(max_length=200)
#     Industry = models.CharField(max_length=200)
#     Commodities = models.CharField(max_length=200)
#     Nation = models.CharField(max_length=200)            # 中国市场、宏观中国、中国监管、中国政府
#     Celebrities = models.CharField(max_length=200)       # 名人新闻
#
#
# class News(models.Model):
#     pass
