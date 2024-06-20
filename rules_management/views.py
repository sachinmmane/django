from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Rule
from .serializers import RuleSerializer, RuleSequenceUpdateSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CreateRuleView(generics.CreateAPIView):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    permission_classes = [IsAuthenticated]

class GetRuleDetailView(generics.RetrieveAPIView):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

class ListRulesView(generics.ListAPIView):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    permission_classes = [IsAuthenticated]

class DeleteRuleView(generics.DestroyAPIView):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

class UpdateRuleView(generics.UpdateAPIView):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


class UpdateRuleSequenceView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = RuleSequenceUpdateSerializer(data=request.data, many=True)
        if serializer.is_valid():
            for item in serializer.validated_data:
                try:
                    rule = Rule.objects.get(pk=item['id'])
                    rule.sequence_id = item['currentIndex']
                    rule.save()
                except Rule.DoesNotExist:
                    return Response({'error': f'Rule with id {item["id"]} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'status': 'Sequence IDs updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)