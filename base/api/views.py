from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from base.serializers import UserSerializer,ConsumerSerializer, WorkerSerializer, JobSerializer, ReviewSerializer, RecieptSerializer, ProblemSerializer, BidSerializer, NotificationSerializer
from base.models import Consumer, Worker, Job, Review, Reciept, Problem, Bids, Notifications
from django.db.models import Q
from django.contrib.auth.models import User

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        return token
        

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def createUser(request):
    user = User.objects.create_user(username = request.data['username'], password = request.data['password'], email = request.data['email'])
    return Response('this model has been created')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def settings(request, pk):
#pk is a boolean passed from the front end as is_worker and if true as implied it creates a worker model else it creates a consumer model
    if pk == 'true':
        user = request.user
        uploaded_file = request.FILES.get('file')
        prof = Worker.objects.create(
            number=request.data['num'],
            bio=request.data['bio'],
            rating=0,
            cv=uploaded_file,
            profile=user
        )
        job = Job.objects.get(name = request.data['job'])
        job.workers.add(prof)
        serializer = WorkerSerializer(prof, many=False)
    else:
        prof = Consumer.objects.create(
            profile=user,
            number=request.data['num'],
            bio=request.data['bio'],
            rating=0
        )
        serializer = ConsumerSerializer(prof, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProblem(request):
    user = request.user
    consumer = Consumer.objects.get(profile = user)
    assigned_job = Job.objects.get(name = request.data['job'])
    problem = Problem.objects.create(
        description = request.data['description'], 
        special_request = request.data['specialRequest'],
        job_type = assigned_job,
        creator = consumer
        )
    problem.save()
    problem_serializer = ProblemSerializer(problem, many = False)
    return Response(problem_serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getWorkers(request, job_id):
    job = Job.objects.get(id = job_id)
    job_serializer = JobSerializer(job, many = False)    
    return Response (job_serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCandidate(request, bid_id):
    bid = Bids.objects.get(id = bid_id)
    candidate = Worker.objects.get(id = bid.bidder.id)
    user = User.objects.get(id = candidate.profile.id)

    user_serializer = UserSerializer(user, many = False)
    candidate_serializer = WorkerSerializer(candidate, many = False)
    info =  [
        candidate_serializer.data,
        user_serializer.data
    ]
    return Response (info)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getJobs(request):
    job = Job.objects.all()
    job_serializer = JobSerializer(job, many = True)
    return Response (job_serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getReciept(request, worker_id):
    user = request.user
    worker = Worker.objects.get(id = worker_id)
    prof = Consumer.objects.get()
    reciept = Reciept.objects.get(Q(employee = worker)| Q(issuer = user)).all()
    reciept_serializer = RecieptSerializer(reciept, many = True)
    #add a way to calculate the total price of all reciepts
    return Response(reciept_serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getReciepts(request):
    user = request.user
    worker = Worker.objects.get(profile = user.id)
    reciepts = worker.reciept_set.all()
    reciept_serializer = RecieptSerializer(reciepts, many = True)
    return Response (reciept_serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancelReciept(request, problem_id):
    problem = Problem.objects.get(id = problem_id)
    reciept  = Reciept.objects.get(work = problem)
    worker = reciept.employee
    notification_value = 'unfortunatelty the reciept of the problem (' + problem.description + ') has been cancelled!, we encourage you to keep your head up and keep looking for more work to do'
    notification = Notifications.objects.create(value = notification_value, profile = worker.profile)
    problem.available = True
    problem.save() 
    reciept.delete()
    notifications_serializer = NotificationSerializer(notification, many = False)
    return Response (notifications_serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createReview(request, worker_id):
    user = request.user
    worker_object = Worker.objects.get(id = worker_id)
    prof = Consumer.objects.get(profile = user)
    review = Review.objects.create(value = request.data['value'], sender = prof.profile.username, worker = worker_object)
    review_serializer = ReviewSerializer(review, many = False)
    return Response (review_serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getReview(request, review_type, worker_get_id):
    user = request.user
    if review_type == 'bids':
        bid = Bids.objects.get(id = worker_get_id)
        worker_id = bid.bidder.id
    elif review_type == 'review': 
        worker_id = worker_get_id
    worker = Worker.objects.get(id = worker_id)
    review = Review.objects.filter(reciever = worker.profile)
    review_serializer = ReviewSerializer(review, many = True)
    return Response (review_serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createBid(request, problem_id):
    user = request.user.id
    if Worker.objects.filter(profile= user).exists():
        worker = Worker.objects.get(profile = user)
        problem = Problem.objects.get(id = problem_id)
        bid = Bids.objects.create(bidder = worker, work = problem, value = request.data['value'], note = request.data['notes'], scheduled_date = request.data['date'])
        bid_serializer = BidSerializer(bid, many = False)

        notification_value = 'you have an unseen bid for the problem (' + problem.description +') go check it out'
        consumer_id = problem.creator.id
        consumer = Consumer.objects.get(id = consumer_id)
        bid = Bids.objects.get(id = bid.id)
        notification = Notifications.objects.create(value = notification_value,profile = consumer.profile, model_id =  bid.id)
        return Response (bid_serializer.data)
    return Response ('this worker does not exist')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBids(request, problem_id):
    work = Problem.objects.get(id = problem_id)
    work_serializer = ProblemSerializer(work, many = False)

    if work.available == False:
        reciept = Reciept.objects.get(work = work)

        reciept_serializer = RecieptSerializer(reciept, many = False)
        info = [
            reciept_serializer.data,
        ]
    else:
        bids = work.bids_set.all()
        information = BidSerializer(bids, many = True)
        info = information.data
    return Response (info)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBid(request, bid_id):
    bid = Bids.objects.get(id = bid_id)
    bid.seen = True
    bid.save()
    bid_serializer = BidSerializer(bid, many = False)
    return Response (bid_serializer.data)


#add a mode
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def acceptBid(request):
    
    user = request.user.id
    bid = Bids.objects.get(id = request.data['bid_id'])
    worker = Worker.objects.get(id = bid.bidder.id)

    problem = Problem.objects.get(id = request.data['prob_id'])
    prof = Consumer.objects.get(profile = user)

    reciept = Reciept.objects.create(issuer = prof, employee = worker, work = problem, price = request.data['price'], scheduled_date = bid.scheduled_date)
    reciept_serializer = RecieptSerializer(reciept, many = False)
    problem.available = False
    problem.save()

    notification = Notifications.objects.create(profile = worker.profile, value = 'your bid was accepted and a reciept has been issued', model_id = reciept.id)
    bid.delete()
    return Response(reciept_serializer.data)


@api_view(['POST'])
def rejectBid(request):
    user = request.user.id
    bid = Bids.objects.get(id = request.data['bid_id'])
    worker = Worker.objects.get(id = bid.bidder.id)

    problem = Problem.objects.get(id = request.data['prob_id'])
    prof = Consumer.objects.get(profile = user)

    notification = Notifications.objects.create(profile = worker.profile, value = 'your bid has been rejected', model_id = problem.id)
    bid.delete()
    return Response('this bid has been deleted')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProblem(request):
    user = request.user
    if Worker.objects.filter(profile = user).exists():
        employee = Worker.objects.get(profile = user)
        job = Job.objects.get(workers = employee.id)
        problems = job.problem_set.filter(available = True)
        problems_serializer = ProblemSerializer(problems, many = True)
        return Response(problems_serializer.data)
    return Response ('this worker does not work')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def consumerData(request):
    user = request.user.id
    if Consumer.objects.filter(profile = user).exists():
        consumer = Consumer.objects.get(profile = user)
        problems = consumer.problem_set.all()
        problem_serializer = ProblemSerializer(problems, many = True)
        return Response (problem_serializer.data)
    else:
        return Response('this consumer model does not exist')


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def getNotifications(request, request_type):
    user = request.user
    notifications = Notifications.objects.filter(profile = user, seen = False)
    notifications_serializer = NotificationSerializer(notifications, many = True)

    if request_type == 'get':
        new_notifications = []
        for notification in notifications:
            notification.seen = True
            notification.save()
            new_notifications.append(notification)
        new_notifications_serializer = NotificationSerializer(new_notifications, many = True)
        return Response (new_notifications_serializer.data)
    return Response (notifications_serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getModelType(request):
    user = request.user.id
    if Consumer.objects.filter(profile = user).exists():
        return Response('consumer')

    elif Worker.objects.filter(profile = user).exists():
        return Response ('worker')
    return Response ('this user does not yet have an assigned role')