from django.shortcuts import render,redirect,get_object_or_404
from .models import Content,DateTime,UserTemp
from .forms import ContentForm,UserTempForm,PasswordForm,ContentReviseForm,TimeRevisingForm,TimeMakingForm
from datetime import datetime,timedelta,time,date

# Create your views here.
def index(request):
    all_contents=Content.objects.all()
    all_timeslots=DateTime.objects.all()

    running_time = []
    for timeslot in all_timeslots:
        timeslot.starttime=timeslot.starttime.strftime('%H:%M:%S')
        timeslot.endtime = timeslot.endtime.strftime('%H:%M:%S')
    #    running_time.append(int(timeslot.endtime[0:2])-int(timeslot.starttime[0:2])+(1/60)*abs(int(timeslot.endtime[3:5])-int(timeslot.starttime[3:5])))
    lst=[]
    for content in all_contents:
        lst.append(content.id)


        
    monday_timeslots=DateTime.objects.filter(day_of_week=0)
    tuesday_timeslots=DateTime.objects.filter(day_of_week=1)
    wednesday_timeslots=DateTime.objects.filter(day_of_week=2)
    thursday_timeslots=DateTime.objects.filter(day_of_week=3)
    friday_timeslots=DateTime.objects.filter(day_of_week=4)
    saturday_timeslots=DateTime.objects.filter(day_of_week=5)
    sunday_timeslots=DateTime.objects.filter(day_of_week=6)


    return render(request,'index.html',{'all_contents':all_contents,'all_timeslots':all_timeslots,
    'monday_timeslots':monday_timeslots,'tuesday_timeslots':tuesday_timeslots,
    'wednesday_timeslots':wednesday_timeslots,'thursday_timeslots':thursday_timeslots,
    'friday_timeslots':friday_timeslots,'saturday_timeslots':saturday_timeslots,'sunday_timeslots':sunday_timeslots,'running_time':running_time})

def create(request):
    if request.method=='POST':
        form=ContentForm(request.POST)
        if form.is_valid():
            obj_content=Content(creator=form.data['creator'],creator_key=form.data['creator_key'],contact=form.data['contact'],title=form.data['title'],department=form.data['department'],location=form.data['location'],reward=form.data['reward'],condition=form.data['condition'],detail=form.data['detail'],password=form.data['password'])
            obj_content.save()
            num_people=int(form.data['num_people'])
            runningdate=int(form.data['runningdate'])
            runningtime=int(form.data['runningtime'])
            date_time=form.data['date']
            for i in range(runningdate):
                date=(datetime.strptime(date_time,'%Y-%m-%d %H:%M:%S')+timedelta(days=i)).date()
                dow=date.weekday()
                for j in range(num_people):
                    starttime=(datetime.strptime(date_time,'%Y-%m-%d %H:%M:%S')+timedelta(minutes=runningtime*j)).time()
                    endtime=(datetime.strptime(date_time,'%Y-%m-%d %H:%M:%S')+timedelta(minutes=runningtime*(j+1))).time()
                    obj_timeslot=DateTime(content=obj_content,date=date,starttime=starttime,endtime=endtime,day_of_week=dow,isUsed=False)
                    obj_timeslot.save()
            return redirect('index')
    content_form=ContentForm()
    return render(request,'create.html',{'content_form':content_form})

def content_detail(request,timeslot_id):
    timeslot=get_object_or_404(DateTime,pk=timeslot_id)
    all_timeslots=DateTime.objects.all()
    timeslots=all_timeslots.filter(content=timeslot_id)
    return render(request,'content_detail.html',{'timeslot':timeslot, 'timeslot_id':timeslot_id})

def content_explain(request, content_id):
    content=get_object_or_404(Content,pk=content_id)
    return render(request,'content_explain.html',{'content':content, 'content_id':content_id})

def enrollment(request,timeslot_id):
    if request.method=='POST':
        filled_form=UserTempForm(request.POST)
        if filled_form.is_valid():
            temp_form=filled_form.save(commit=False)
            temp_form.time_temp=DateTime.objects.get(pk=timeslot_id)
            temp_form.save()

            timeslot=DateTime.objects.get(pk=timeslot_id)
            timeslot.isUsed=True
            timeslot.save()

            return redirect('index')

    timeslot=DateTime.objects.get(pk=timeslot_id)
    usertemp=UserTempForm()
    if timeslot.isUsed==False:
        return render(request,'usertemp.html',{'usertemp':usertemp,'timeslot':timeslot}) #timeslot.id에서 timeslot으로 수정
    if timeslot.isUsed==True:
        return redirect('time_admin',timeslot.id)

def time_detail(request,content_id):
    content=get_object_or_404(Content,pk=content_id)
    all_timeslots=DateTime.objects.all()
    timeslots=all_timeslots.filter(content=content_id)
    return render(request,'time_detail.html',{'timeslots':timeslots, 'content_id':content_id}) #content_id추가


def content_admin(request,content_id):
    passwordform=PasswordForm()
    content_id=content_id
    if request.method=="POST":
        passwordform=PasswordForm(request.POST)
        password_temp=passwordform.data['password_temp']
        content=Content.objects.get(pk=content_id)
        if int(content.password)==int(password_temp):
            content=get_object_or_404(Content,pk=content_id)
            all_timeslots=DateTime.objects.all()
            timeslots=all_timeslots.filter(content=content_id)
            content_form=ContentReviseForm(instance=content)
            # if request.method=="POST":
            #     updated_form=ContentAdviseForm(request.POST,instance=content) 
            #     if updated_form.is_valid():
            #         content.title=updated_form.data['title']
            #         content.save()
            #         return redirect('index')
            return render(request,'time_detail_for_creator.html',{'timeslots':timeslots,'content_form':content_form,'content_id':content.id})
        else:
            return render(request,'password_content.html',{'passwordform':passwordform,'content_id':content_id})
    return render(request,'password_content.html',{'passwordform':passwordform,'content_id':content_id})

def time_admin(request,timeslot_id):
    passwordform=PasswordForm()
    if request.method=="POST":
        passwordform=PasswordForm(request.POST)
        password_temp=passwordform.data['password_temp']

        timeslot=DateTime.objects.get(pk=timeslot_id)
        try:
            usertemp_obj=UserTemp.objects.get(time_temp=timeslot)
        except:
            return render(request,'password_time.html',{'passwordform':passwordform})

        if int(usertemp_obj.password)==int(password_temp):
            timeslot=DateTime.objects.get(pk=timeslot_id)
            user=UserTemp.objects.get(time_temp=timeslot)
            usertemp_form=UserTempForm(instance=user)
            # if request.method=="POST":
            #     updated_form=UserTempForm(request.POST,instance=user) 
            #     if updated_form.is_valid():
            #         updated_form.save()
            #         return redirect('index')
            return render(request,'usertemp_revise.html',{'usertemp':usertemp_form,'timeslot':timeslot}) #timeslot.id에서 timeslot
        else:
            return render(request,'password_time.html',{'passwordform':passwordform})
    return render(request,'password_time.html',{'passwordform':passwordform})

def content_revise(request,content_id):
    content=Content.objects.get(pk=content_id)
    if request.method=="POST":
            updated_form=ContentReviseForm(request.POST,instance=content) 
            if updated_form.is_valid():
                    content.title=updated_form.data['title']
                    content.contact=updated_form.data['contact']
                    content.title=updated_form.data['title']
                    content.department=updated_form.data['department']
                    content.reward=updated_form.data['reward']
                    content.condition=updated_form.data['condition']
                    content.detail=updated_form.data['detail']
                    content.location=updated_form.data['location']
                    content.save()
                    return redirect('index')

def user_revise(request,timeslot_id):
    timeslot=DateTime.objects.get(pk=timeslot_id)
    user=UserTemp.objects.get(time_temp=timeslot)
    usertemp_form=UserTempForm(instance=user)
    if request.method=="POST":
        updated_form=UserTempForm(request.POST,instance=user) 
        if updated_form.is_valid():
            updated_form.save()
            return redirect('index')    

# def advise(request,timeslot_id):
#     timeslot=DateTime.objects.get(pk=timeslot_id)
#     user=UserTemp.objects.get(time_temp=timeslot)
#     usertemp_form=UserTempForm(instance=user)
#     if request.method=="POST":
#         updated_form=UserTempForm(request.POST,instance=user) 
#         if updated_form.is_valid():
#             updated_form.save()
#             return redirect('index')
#     return render(request,'usertemp_advise.html',{'usertemp':usertemp_form,'timeslot':timeslot.id})

def time_revise(request,timeslot_id,content_id):
    content=get_object_or_404(Content,pk=content_id)
    all_timeslots=DateTime.objects.all()
    timeslots=all_timeslots.filter(content=content_id)
    content_form=ContentReviseForm(instance=content)     

    timeslot=DateTime.objects.get(pk=timeslot_id)
    timetemp_form=TimeMakingForm(instance=timeslot)
    if request.method=="POST":
        updated_form=TimeMakingForm(request.POST,instance=timeslot)
        if updated_form.is_valid():
            updated_form.save()
            return render(request,'time_detail_for_creator.html',{'timeslots':timeslots,'content_form':content_form,'content_id':content.id})

    if timeslot.isUsed==False:
        return render(request, 'time_revise.html',{'timetemp_form':timetemp_form, 'timeslot':timeslot}) #timeslot도 받아오기
    else:
        return render(request,'time_detail_for_creator.html',{'timeslots':timeslots,'content_form':content_form,'content_id':content.id})

def maker(request):
    return render(request, 'maker.html')

def content_delete(request,content_id):
    if request.method=="POST":
        content=Content.objects.get(pk=content_id)
        content.delete()

        return redirect('index')

def time_delete(request,timeslot_id):
    timeslot=DateTime.objects.get(pk=timeslot_id)
    timeslot.isUsed=False
    timeslot.save()
    user=UserTemp.objects.get(time_temp=timeslot)
    user.delete()

    return redirect('index')

def time_make(request,content_id):
    if request.method=='POST':
        form=TimeMakingForm()
        return render(request,'time_make.html',{'form':form,'content_id':content_id})
def time_make_save(request,content_id):
    if request.method=='POST':
        form=TimeMakingForm(request.POST)
        if form.is_valid():
            content=get_object_or_404(Content,pk=content_id)
            all_timeslots=DateTime.objects.all()
            timeslots=all_timeslots.filter(content=content_id)
            content_form=ContentReviseForm(instance=content) 

            content_temp=Content.objects.get(pk=content_id)
            date_temp=form.data['date']
            date=datetime.strptime(date_temp,'%Y-%m-%d')
            dow=date.weekday()
            obj_date=DateTime(content=content_temp,date=date,day_of_week=dow,starttime=form.data['starttime'],endtime=form.data['endtime'],isUsed=False)
            obj_date.save()
            
            return render(request,'time_detail_for_creator.html',{'timeslots':timeslots,'content_form':content_form, 'content_id':content.id})

def close(request,timeslot_id,content_id):
    if request.method=="POST": 
        content=get_object_or_404(Content,pk=content_id)
        all_timeslots=DateTime.objects.all()
        timeslots=all_timeslots.filter(content=content_id)
        content_form=ContentReviseForm(instance=content)    
        
        timeslot=DateTime.objects.get(pk=timeslot_id)
        if timeslot.isUsed==False:
            timeslot.delete()
        return render(request,'time_detail_for_creator.html',{'timeslots':timeslots,'content_form':content_form, 'content_id':content.id})
        


