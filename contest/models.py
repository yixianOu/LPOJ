# -*- coding: utf-8 -*-
from django.db import models


class ContestInfo(models.Model):

    creator = models.CharField(max_length=50, default="admin")
    oj = models.CharField(max_length=50, default="LPOJ")
    title = models.CharField(max_length=50, default="contest")
    level = models.IntegerField(default=1)
    des = models.CharField(max_length=500, default="contest des")
    note = models.CharField(max_length=500, default="contest note")
    begintime = models.DateTimeField()
    lasttime = models.IntegerField(default=18000)
    type = models.CharField(max_length=50, default="ACM")
    auth = models.IntegerField(default=2)  # 1 public 2 private 0 protect(需注册)
    clonefrom = models.IntegerField(default=-1)
    classes = models.CharField(max_length=500, default="All")
    iprange = models.CharField(max_length=2000, default="iprange")

    lockboard = models.IntegerField(default=0) # 0 不封 1 封
    locktime = models.IntegerField(default=0) # 最后多少分钟封榜

    objects = models.Manager()

    def __str__(self):
        return self.creator


class ContestAnnouncement(models.Model):

    contestid = models.IntegerField()
    announcement = models.CharField(max_length=500)

    objects = models.Manager()

    def __str__(self):
        return self.contestid


class ContestProblem(models.Model):

    contestid = models.IntegerField()
    problemid = models.CharField(max_length=50)
    problemtitle = models.CharField(max_length=500, default="uname")
    rank = models.IntegerField()  # 顺序

    objects = models.Manager()

    def __str__(self):
        return self.contestid




class ContestBoard(models.Model):

    contestid = models.IntegerField()
    username = models.CharField(max_length=50)
    user = models.CharField(max_length=50)
    problemrank = models.IntegerField()
    type = models.IntegerField()  # 1 AC， 0没AC算罚时，-1没AC不算罚时, 2 封榜中，不算罚时(只会在后端做修改)
    submittime = models.BigIntegerField()  # 豪秒为单位
    submitid = models.IntegerField()  # 用于rejudge
    rating = models.IntegerField(default=1500)

    objects = models.Manager()

    def __str__(self):
        return self.contestid


class ContestComment(models.Model):

    contestid = models.IntegerField()
    user = models.CharField(max_length=50)
    title = models.CharField(max_length=50, default="提问")
    problem = models.CharField(default='ALL', max_length=500)  # 对哪个题目提问
    message = models.CharField(max_length=500)
    huifu = models.CharField(default="No respones", max_length=500)
    time = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=1500)

    objects = models.Manager()

    def __str__(self):
        return self.contestid

class ContestTutorial(models.Model):

    contestid = models.IntegerField()
    value = models.TextField(default="暂无数据！")

    objects = models.Manager()

    def __str__(self):
        return self.contestid


class ContestRegister(models.Model):

    contestid = models.IntegerField()
    user = models.CharField(max_length=50)
    rating = models.IntegerField(default=0)

    objects = models.Manager()

    def __str__(self):
        return self.contestid


class ContestRatingChange(models.Model):

    contestid = models.IntegerField()
    contestname = models.CharField(max_length=100)
    contesttime = models.CharField(max_length=100)
    user = models.CharField(max_length=50)
    lastrating = models.IntegerField(default=0)
    ratingchange = models.IntegerField(default=0)
    currentrating = models.IntegerField(default=0)

    objects = models.Manager()

    def __str__(self):
        return self.contestid


class ContestComingInfo(models.Model):

    ojName = models.CharField(max_length=100)
    link = models.CharField(max_length=200)
    startTime = models.BigIntegerField()
    endTime = models.BigIntegerField()
    contestName = models.CharField(max_length=500)

    objects = models.Manager()

    def __str__(self):
        return self.contestName


class ContestBoardTotal(models.Model):

    user = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    contestid = models.IntegerField()
    score = models.IntegerField()
    time = models.CharField(max_length=100)
    detail = models.CharField(max_length=500) # |

    objects = models.Manager()

    def __str__(self):
        return self.user

class ContestChoiceProblem(models.Model):

    ContestId = models.IntegerField()
    ChoiceProblemId = models.CharField(max_length=50)
    rank = models.IntegerField()  # 顺序

    objects = models.Manager()

    def __str__(self):
        return self.ContestId

class StudentChoiceAnswer(models.Model):
    username = models.CharField(max_length=100,default="")
    realname = models.CharField(max_length=100,default="")
    number = models.CharField(max_length=100,default="")
    contestid = models.CharField(max_length=100,default="")
    answer = models.CharField(max_length=100)
    answer_detail = models.TextField(default="")
    score = models.IntegerField()

    objects = models.Manager()

    def __str__(self):
        return self.user

