from configparser import SectionProxy
from azure.identity import DeviceCodeCredential
from msgraph.generated.users.item.user_item_request_builder import UserItemRequestBuilder
from msgraph.generated.models.item_body import ItemBody
from msgraph import GraphServiceClient
from msgraph.generated.models.chat_message import ChatMessage
from msgraph.generated.models.call import Call
from msgraph.generated.models.invitation_participant_info import InvitationParticipantInfo
from msgraph.generated.models.identity_set import IdentitySet
from msgraph.generated.models.identity import Identity
from msgraph.generated.models.modality import Modality
from msgraph.generated.models.outgoing_call_options import OutgoingCallOptions
from msgraph.generated.models.service_hosted_media_config import ServiceHostedMediaConfig


class Graph:
    settings: SectionProxy
    device_code_credential: DeviceCodeCredential
    user_client: GraphServiceClient

    def __init__(self, config: SectionProxy):
        self.settings = config
        client_id = self.settings['clientId']
        tenant_id = self.settings['tenantId']
        graph_scopes = self.settings['graphUserScopes'].split(' ')

        self.device_code_credential = DeviceCodeCredential(client_id, tenant_id = tenant_id)
        self.user_client = GraphServiceClient(self.device_code_credential, graph_scopes)

    async def get_user_token(self):
        graph_scopes = self.settings['graphUserScopes']
        access_token = self.device_code_credential.get_token(graph_scopes)
        with open('api_token_access.tok', 'w') as _f:
            _f.write(access_token.token)
        return access_token.token

    async def get_user(self):
        # Only request specific properties using $select
        query_params = UserItemRequestBuilder.UserItemRequestBuilderGetQueryParameters(
            select=['displayName', 'mail', 'userPrincipalName']
        )

        request_config = UserItemRequestBuilder.UserItemRequestBuilderGetRequestConfiguration(
            query_parameters=query_params
        )

        user = await self.user_client.me.get(request_configuration=request_config)
        return user

    async def make_graph_call(self, uid):
        #pobranie danych użytkownika na podstawie ID
        print('id:', id)
        result = await self.user_client.users.by_user_id(uid).get()
        print(result)
        return

    async def make_graph_call_2(self):
        #pobranie danych myself
        result = await self.user_client.me.get()
        print(result)
        return

    async def make_graph_call_3(self):
        #pobranie listy chatów uzytkownika
        result = await self.user_client.chats.get()
        print(result)
        return

    async def make_graph_call_4(self, uid):
        #pobranie konkretnego chatu by ID
        result = await self.user_client.teams.by_team_id(uid).get()
        print(result)
        return

    async def make_graph_call_5(self, msg, uid):
        #wysłanie message do chatu o id
        request_body = ChatMessage(
            body = ItemBody(
                content={msg}
            )
        )
        result = await self.user_client.chats.by_chat_id(uid).messages.post(request_body)
        print(result)
        return

    async def make_graph_call_6(self, uid):
        #pobranie użytkowników czatu
        result = await self.user_client.chats.by_chat_id(uid).members.get()
        print(result)
        return

    async def make_graph_call_7(self, name, uid):
        #dzwonienie do usera
        request_body = Call(
            odata_type="#microsoft.graph.call",
            callback_uri="https://bot.contoso.com/callback",
            targets=[
                InvitationParticipantInfo(
                    odata_type="#microsoft.graph.invitationParticipantInfo",
                    identity=IdentitySet(
                        odata_type="#microsoft.graph.identitySet",
                        user=Identity(
                            odata_type="#microsoft.graph.identity",
                            display_name="{name}",
                            id="{uid}",
                        ),
                    ),
                ),
            ],
            requested_modalities=[
                Modality.Audio,
            ],
            call_options=OutgoingCallOptions(
                odata_type="#microsoft.graph.outgoingCallOptions",
                is_content_sharing_notification_enabled=True,
                is_delta_roster_enabled=True,
            ),
            media_config=ServiceHostedMediaConfig(
                odata_type="#microsoft.graph.serviceHostedMediaConfig",
            ),
        )

        result = await self.user_client.communications.calls.post(request_body)
        print(result)
        return




