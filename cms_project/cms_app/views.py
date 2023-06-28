from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from .models import User, Post, Like
from .serializers import UserSerializer,GetalluserSerializer, PostSerializer, LikeSerializer,PostPutSerializer,PostpSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(password)

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CreateUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RetriveallUserView(APIView): 
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = User.objects.all()
            serializer = GetalluserSerializer(user,many=True)
            context = {
                'status':status.HTTP_200_OK,
                'success':True,
                'response':serializer.data
                }
            return Response(context, status=status.HTTP_200_OK)
        except Exception as exception:
            context = {
                'status':status.HTTP_400_BAD_REQUEST,
                'success':False,
                'response':str(exception)
            }
            return Response(context,status=status.HTTP_400_BAD_REQUEST)


class ReadUpdateDeleteUserView(APIView): 
   

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
  
    def put(self, request, user_id):
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            if user:
                user.delete()
                context = {
                        "status":status.HTTP_200_OK,
                        "success":True,
                        "response":"Successfully removed User"
                    }
                return Response(context,status=status.HTTP_200_OK)
            else:
                context = {
                    "status":status.HTTP_200_OK,
                    "success":True,
                    "response":"Already removed User"
                }
                return Response(context,status=status.HTTP_200_OK)
             
        except User.DoesNotExist:
            context = {
                'status':status.HTTP_200_OK,
                'success':False,
                'response':"Does Not Exist User!"
            }
            return Response(context,status=status.HTTP_200_OK)


        except Exception as exception:
            context = {
                'status':status.HTTP_400_BAD_REQUEST,
                'success':False,
                'response':str(exception)
            }
            return Response(context,status=status.HTTP_400_BAD_REQUEST)


class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            serializer = PostpSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=request.user)

                context = {
                'status':status.HTTP_201_CREATED,
                'success':True,
                'response':serializer.data
                }
                return Response(context, status=status.HTTP_201_CREATED)
        except Exception as exception:
            context = {
                'status':status.HTTP_400_BAD_REQUEST,
                'success':False,
                'response':str(exception)
            }
            return Response(context,status=status.HTTP_400_BAD_REQUEST)
           

class RetriveAllPostView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            post = Post.objects.all()
            serializer = PostSerializer(post,many=True)
            context = {
                'status':status.HTTP_200_OK,
                'success':True,
                'response':serializer.data
                }
            return Response(context,status=status.HTTP_200_OK)
        except Exception as exception:
            context = {
                'status':status.HTTP_400_BAD_REQUEST,
                'success':False,
                'response':str(exception)
            }
            return Response(context,status=status.HTTP_400_BAD_REQUEST)


class ReadUpdateDeletePostView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            if post.is_accessible_by(request.user):
                serializer = PostSerializer(post)
                context = {
                'status':status.HTTP_200_OK,
                'success':True,
                'response':serializer.data
                }
                
                return Response(context,status=status.HTTP_200_OK)
            else:
                context = {
                'status':status.HTTP_403_FORBIDDEN,
                'success':True,
                'response':'Access denied'
                }
                return Response(context, status=status.HTTP_403_FORBIDDEN)
        except Post.DoesNotExist:
            context = {
                'status':status.HTTP_404_NOT_FOUND,
                'success':True,
                'response':"Does not Exist post"
            }
            return Response(context,status=status.HTTP_404_NOT_FOUND)
            
        except Exception as exception:
            context = {
                'status':status.HTTP_400_BAD_REQUEST,
                'success':False,
                'response':str(exception)
            }
            return Response(context,status=status.HTTP_400_BAD_REQUEST)
        
    
    permission_classes = [IsOwnerOrReadOnly]
    def put(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            if post.owner != request.user:
                return Response({'message': 'You are not the owner of this post'}, status=status.HTTP_403_FORBIDDEN)
            serializer = PostPutSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                context = {
                'status':status.HTTP_200_OK,
                'success':True,
                'response':"Successfully Update"
                }
                
                return Response(context,status=status.HTTP_200_OK)

            
        except Post.DoesNotExist:
            context = {
                'status':status.HTTP_404_NOT_FOUND,
                'success':True,
                'response':"Does not Exist post"
            }
            return Response(context,status=status.HTTP_404_NOT_FOUND)
            
        except Exception as exception:
            context = {
                'status':status.HTTP_400_BAD_REQUEST,
                'success':False,
                'response':str(exception)
            }
            return Response(context,status=status.HTTP_400_BAD_REQUEST)
    

    
    permission_classes = [IsOwnerOrReadOnly]
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            if post.owner != request.user:
                return Response({'message': 'You are not the owner of this post'}, status=status.HTTP_403_FORBIDDEN)
            else:
                post.delete()
                return Response({'message': 'Successfully Delete'}, status=status.HTTP_200_OK)
            
        except Post.DoesNotExist:
            context = {
                'status':status.HTTP_404_NOT_FOUND,
                'success':True,
                'response':"Does Not Exist Post"
            }
            return Response(context,status=status.HTTP_404_NOT_FOUND)
            
        except Exception as exception:
            context = {
                'status':status.HTTP_400_BAD_REQUEST,
                'success':False,
                'response':str(exception)
            }
            return Response(context,status=status.HTTP_400_BAD_REQUEST)

            


class CreateLikeView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            serializer = LikeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                context = {
                'status':status.HTTP_200_OK,
                'success':True,
                'response':"Successfully Like"
                }
                return Response(context, status=status.HTTP_200_OK)
            else:
                context = {
                'status':status.HTTP_404_NOT_FOUND,
                'success':False,
                'response':"Does not Exist Post"
                }
                return Response(context, status=status.HTTP_404_NOT_FOUND)
       
            
        except Exception as exception:
            context = {
                'status':status.HTTP_400_BAD_REQUEST,
                'success':False,
                'response':str(exception)
            }
            return Response(context,status=status.HTTP_400_BAD_REQUEST)

class RetriveallLikeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            like = Like.objects.all()
            serializer = LikeSerializer(like,many=True)
           
            context = {
                    'status':status.HTTP_200_OK,
                    'success':True,
                    'response':serializer.data
                    }
            return Response(context, status=status.HTTP_200_OK)
            
        except Exception as exception:
            context = {
                'status':status.HTTP_400_BAD_REQUEST,
                'success':False,
                'response':str(exception)
            }
            return Response(context,status=status.HTTP_400_BAD_REQUEST)
    
class ReadUpdateDeleteLikeView(APIView):
   

    def get(self, request, like_id):
        like = Like.objects.get(id=like_id)
        serializer = LikeSerializer(like)
        return Response(serializer.data)
    

    
    permission_classes = [IsAuthenticated]
    def put(self, request, like_id):
        try:
            like = Like.objects.get(id=like_id)
            serializer = LikeSerializer(like, data=request.data)
            if serializer.is_valid():
                serializer.save()
                context = {
                'status':status.HTTP_200_OK,
                'success':True,
                'response':"Successfully Update Like"
                }
                return Response(context,status=status.HTTP_200_OK)
            
            
        except Exception as exception:
            context = {
                'status':status.HTTP_400_BAD_REQUEST,
                'success':False,
                'response':str(exception)
            }
            return Response(context,status=status.HTTP_400_BAD_REQUEST)

   
    def delete(self, request, like_id):
        
        try: 

            like = Like.objects.get(id=like_id)
        
            if like:
                like.delete()
                context = {
                    "status":status.HTTP_200_OK,
                    "success":True,
                    "response":"Successfully removed like "
                }
                return Response(context,status=status.HTTP_200_OK)
            else:
                context = {
                    "status":status.HTTP_200_OK,
                    "success":True,
                    "response":"Already removed your like!"
                }
                return Response(context,status=status.HTTP_200_OK)
            
        except Like.DoesNotExist:
            context = {
                'status':status.HTTP_404_NOT_FOUND,
                'success':True,
                'response':"Does not Exist like !"
            }
            return Response(context,status=status.HTTP_404_NOT_FOUND)


        except Exception as exception:
            context = {
                'status':status.HTTP_400_BAD_REQUEST,
                'success':False,
                'response':str(exception)
            }
            return Response(context,status=status.HTTP_400_BAD_REQUEST)
