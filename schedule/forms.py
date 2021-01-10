from .models import Content,DateTime,UserTemp
from django import forms
import datetime

from django.utils.translation import gettext_lazy as _

class ContentForm(forms.Form):
    title=forms.CharField(label="실험 제목",max_length=50)

    creator=forms.CharField(label="실험 주최자",max_length=50)
    creator_key=forms.IntegerField(label="사용자 키",widget=forms.NumberInput(attrs={'placeholder':'학번 입력'}))
    contact=forms.CharField(label="연락처", widget=forms.Textarea(attrs={'placeholder':'전화번호와 이메일을 남겨주세요.','class':'contact'}))

    department=forms.CharField(label="학부",max_length=50)
    
    date=forms.DateTimeField(
        label="실험 날짜",initial=datetime.datetime.now(),widget=forms.DateTimeInput(attrs={'class':'datetimepicker'}))
    runningdate=forms.IntegerField(label="실험 진행 일수")

    runningtime=forms.IntegerField(label='한번 실험 걸리는 시간',widget=forms.NumberInput(attrs={'placeholder':'분 단위로 입력','class':'timepicker'}))
    location=forms.CharField(label="지역",max_length=50)

    num_people=forms.IntegerField(label="실험 인원 수")
    reward=forms.CharField(label="실험 보수",max_length=50)

    condition=forms.CharField(label="실험 자격 조건",widget=forms.Textarea)
    detail=forms.CharField(label="실험 설명",widget=forms.Textarea)

    password=forms.IntegerField()

class PasswordForm(forms.Form):
    password_temp=forms.IntegerField(label="실험 신청 시 입력한 비밀번호")

class UserTempForm(forms.ModelForm):

    class Meta:
        model=UserTemp
        fields=('name','major','num_student','num_phone','num_account','password')
        labels={
            'name': _('이름'),
            'major': _('전공'),
            'num_student': _('학번'),
            'num_phone': _('전화번호'),
            'num_account': _('계좌번호'),
            'password':_('비밀번호'),
        }
        widgets={
            'password': forms.NumberInput(attrs={'placeholder':'이후 신청 수정 시 필요'}),
            'num_account': forms.NumberInput(attrs={'placeholder':'경남은행 계좌 입력'})
        }

class TimeMakingForm(forms.ModelForm):
    class Meta:
        model=DateTime
        fields=('date','starttime','endtime')

class TimeRevisingForm(forms.ModelForm):
    class Meta:
        model=DateTime
        fields=('starttime','endtime')
        labels={
            'starttime': _('시작 시간'),
            'endtime': _('끝나는 시간'),
        }

        widgets={
            'starttime': forms.TimeInput(attrs={'class':'starttime'}),
            'endtime': forms.TimeInput(attrs={'class':'endtime'})
        }

class ContentReviseForm(forms.ModelForm):
    class Meta:
        model=Content
        fields=('creator','contact','title','department','reward','condition','detail','location')

        labels={
            'creator': _('제작자'),
            'contact': _('연락처'),
            'title': _('실험 제목'),
            'department': _('학부'),
            'reward': _('보수'),
            'condition': _('실험 자격'),
            'detail': _('실험 상세 설명'),
            'location': _('실험 장소'),
        }

