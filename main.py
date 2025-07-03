import asyncio
import configparser
from msgraph.generated.models.o_data_errors.o_data_error import ODataError
from graph import Graph
import urllib3

async def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    print('Python Graph Test\n')

    # Load settings
    config = configparser.ConfigParser()
    config.read(['config.cfg', 'config.dev.cfg'])
    azure_settings = config['azure']

    graph: Graph = Graph(azure_settings)

    await greet_user(graph)

    choice = -1

    while choice != 0:
        print('Please choose one of the following options:')
        print('0. Exit')
        print('1. Display access token')
        print('2. Get user properties by ID')
        print('3. Get my properties')
        print('4. Get list of chats by user ID')
        print('5. Get chat by ID')
        print('6. Send message to chat')
        print('7. Get chat users')
        print('8. Call to user')

        try:
            choice = int(input())
        except ValueError:
            choice = -1

        try:
            if choice == 0:
                print('Goodbye...')
            elif choice == 1:
                await display_access_token(graph)
            elif choice == 2:
                await make_graph_call(graph)
            elif choice == 3:
                await make_graph_call_2(graph)
            elif choice == 4:
                await make_graph_call_3(graph)
            elif choice == 5:
                await make_graph_call_4(graph)
            elif choice == 6:
                await make_graph_call_5(graph)
            elif choice == 7:
                await make_graph_call_6(graph)
            elif choice == 8:
                await make_graph_call_7(graph)
            else:
                print('Invalid choice!\n')
        except ODataError as odata_error:
            print('Error:')
            if odata_error.error:
                print(odata_error.error.code, odata_error.error.message)

async def greet_user(graph: Graph):
    user = await graph.get_user()
    if user:
        print('Hello,', user.display_name)
        print('Email:', user.mail or user.user_principal_name, '\n')

async def display_access_token(graph: Graph):
    token = await graph.get_user_token()
    print('User token:', token, '\n')

async def make_graph_call(graph: Graph):
    user = await graph.get_user()
    if user:
        print('Hello,', user.id)
    await graph.make_graph_call(user.id)

async def make_graph_call_2(graph: Graph):
    await graph.make_graph_call_2()

async def make_graph_call_3(graph: Graph):
    await graph.make_graph_call_3()

async def make_graph_call_4(graph: Graph):
    await graph.make_graph_call_4()

async def make_graph_call_5(graph: Graph):
    await graph.make_graph_call_5()

async def make_graph_call_6(graph: Graph):
    await graph.make_graph_call_6()

async def make_graph_call_7(graph: Graph):
    await graph.make_graph_call_7()


asyncio.run(main())
