import requests
import time
# token vk
token = ""
# Функция получения подписчиков группы
def get_users(nodes):
    url = "https://api.vk.com/method/groups.getMembers?"
    # id группы «Сгу факультет КНиИТ» и «Душевно»
    id = ["49520224", "159306320"]
    for group_id in id:
        # Смещение, необходимое для выборки 
        # определённого подмножества участников
        offset = 0
        # Количество участников сообщества, которое получим (1000 = max)
        count_subscribes = 1000 
        while (True):
            params = dict(access_token=token, group_id = group_id, 
                        offset = offset, count = count_subscribes, v = 5.131)
            request = requests.get(url, params = params)
            data = request.json()
            if (data['response']['items']):
                offset += count_subscribes
            else:
                break
            for user in data['response']['items']:
                nodes[user] = dict()
            # Задержка, так как можно делать только 3 запроса в секунду 
            time.sleep(0.5)
# Функция получения данных у пользователя
def get_profile_info(nodes):
    url = "https://api.vk.com/method/users.get?"
    for user in nodes:
        params = dict(access_token=token, user_id=user, 
                      fields = "bdate,home_town,sex,followers_count",v=5.131)
        request = requests.get(url, params=params)
        data = request.json()
        nodes[user] = data['response'][0]
        time.sleep(0.5)
# Функция получения друзей у подписчиков
def get_friends(nodes, edges):
    url = "https://api.vk.com/method/friends.get?"
    for user in nodes:
        params = dict(access_token=token, user_id = user, v=5.131)
        request = requests.get(url, params = params)
        data = request.json()
        # Пользователь закрыл своих друзей
        if ("response" not in data):
            continue
        for friend in data['response']['items']:
            if (friend in nodes):
                edge = dict(source = user, target = friend)
                edges.append(edge)
        time.sleep(0.5)
# Функция создания файлов nodes.csv и edges.csv, которые
# используются в Gephi для отрисовки анализа графа
def create_graph(nodes, edges):
    file = open("./node.csv",'w', encoding = 'utf8')
    file.write("id\tlabel\tfollowers_count\tbdate\tsex\thome_town\n")
    for node in nodes.values():
        file.write(f"{node['id']}\t{node['first_name']} "
                   f"{node['last_name']}\t{node['followers_count']}"
                   f"\t{node['bdate']}\t{node['sex']}\t{node['home_town']}\n")
    file.close()
    file = open("./edges.csv", 'w', encoding='utf8')
    file.write("source;target\n")
    for edge in edges:
        file.write(f"{edge['source']};{edge['target']}\n")
    file.close()
def main():
    nodes = dict()
    edges = list()
    get_users(nodes)
    get_profile_info(nodes)
    get_friends(nodes, edges)
    create_graph(nodes,edges)
if __name__ == "__main__":
    main()