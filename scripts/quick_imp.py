import socket
import glob

host = "127.0.0.1"
port = 12000
orig_folder = 'exp_res\\processed_motiondata\\free_talk_couples'

def main():
    # connection
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    # read file
    files = glob.glob(orig_folder + '\\*.*')
    file = files[0]
    print(file)
    with open(file, 'r') as f:
        for line in f:
            vals = line[1:-1].splilt(',')
            command = f'moveaxis 1 {vals[0]} 2 {vals[1]} 3 {vals[2]} 4 {vals[4]}'
            # send
            client.send(command)
    # close
    client.close()

if __name__ == '__main__':
    main()