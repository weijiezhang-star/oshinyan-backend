from django.conf import settings

# For Define API Views
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import  Shop, ShopImage, CatApplication
from .serializers import ShopSerializer, ShopImageSerializer, CatApplicationSerializer

from .email_templates import cat_register_email

# For ElasticEmail
import ElasticEmail
from ElasticEmail.api import emails_api
from ElasticEmail.model.email_content import EmailContent
from ElasticEmail.model.body_part import BodyPart
from ElasticEmail.model.body_content_type import BodyContentType
from ElasticEmail.model.email_recipient import EmailRecipient
from ElasticEmail.model.email_message_data import EmailMessageData

configuration = ElasticEmail.Configuration()
configuration.api_key['apikey'] = settings.MAIL_API_KEY

def send_email(reciever_email, subject, content):
    with ElasticEmail.ApiClient(configuration) as api_client:
            api_instance = emails_api.EmailsApi(api_client)
            email_message_data = EmailMessageData(
                recipients=[
                    EmailRecipient(
                        email=reciever_email,
                    ),
                ],
                content=EmailContent(
                    body=[
                        BodyPart(
                            content_type=BodyContentType("HTML"),
                            content=content,
                            charset="utf-8",
                        ),
                    ],
                    _from=settings.BACKEND_EMAIL,
                    reply_to=settings.BACKEND_EMAIL,
                    subject=subject,
                ),
            )
            api_instance.emails_post(email_message_data)

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    def create(self, request, *args, **kwargs):
        shop_data = self.get_serializer(data=request.data)
        images = request.FILES.getlist('imgs')
        shop_name = request.data.get('shop_name')
        
        if shop_data.is_valid():
            if not Shop.objects.filter(shop_name=shop_name).exists():
                item = shop_data.save()
                for image in images:
                    ShopImage.objects.create(shop_id=item.id, imgs=image)
                
                send_email(shop_data.data['email'], "看板猫！発見御礼にゃ！", "<p>" + shop_data.data['shop_name'] + "様</p>" + cat_register_email)
                send_email(settings.BACKEND_EMAIL, '看板猫　登録依頼にゃ！',
                           f"""
                                <p>事務局担当者</p>
                                <p>
                                    「推しニャン」サイトに看板猫発見の依頼がありました。<br/>
                                    下記ご確認ください。
                                </p>
                                <p>日時：{shop_data.data['last_update']}</p>
                                <p>
                                    <span>店舗名：{shop_data.data['shop_name']}</span><br />
                                    <span>住所：{shop_data.data['prefecture'], shop_data.data['city'], shop_data['street'], shop_data.data['detail_address']}</span><br />
                                    <span>メールアドレス：{shop_data.data['email']}</span><br />
                                    <span>電話：{shop_data.data['phone']}</span><br />
                                    <span>店舗許諾：{shop_data.data['shop_permission']}</span><br />
                                    <span>看板猫情報：{shop_data.data['cat_info']}</span>
                                </p>
                                <p>以上です。</p>
                            """
                        )
                
                return Response(shop_data.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'errors': shop_data.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class ShopImageViewSet(viewsets.ModelViewSet):
    queryset = ShopImage.objects.all()
    serializer_class = ShopImageSerializer

class CatApplicationViewSet(viewsets.ModelViewSet):
    queryset = CatApplication.objects.all()
    serializer_class = CatApplicationSerializer