from paramiko import SSHClient, AutoAddPolicy
from json import load
from argparse import ArgumentParser


class SSH:
    """
    La classe SSH permet d'instancier une connexion SSH, de s'y connecter
    et d'y exécuter des commandes !
    """

    def __init__(self):
        self.instance = SSHClient()
        self.add_key
        self.connect_to_ssh

    @property
    def credentials(self):
        with open('credentials.json', 'r') as cred:
            cred = load(cred)['ssh']
            return cred['domain'], int(cred['port']), cred['username'], cred['password']

    @property
    def connect_to_ssh(self):
        """
        connect_to_ssh permet de créer une socket entre le client et le serveur !
        La connexion restera active tant que l'instance sera existante !
        """
        return self.instance.connect(
            hostname=self.credentials[0],
            port=self.credentials[1],
            username=self.credentials[2],
            password=self.credentials[3]
        )

    @property
    def add_key(self):
        """
        add_key permet de créer une clé SSH nécessaire au fonctionnement du protocol.
        La clé s'ajoute dans le known_hosts !
        """
        return self.instance.set_missing_host_key_policy(AutoAddPolicy())

    @property
    def close(self):
        """
        close ferme la connexion SSH
        :return:
        """
        return self.instance.close()

    def execute_command(self, command: str):
        """
        Return a string if the instruction return something, else None (executed in the OS stack)
        :return: str
        """
        return self.instance.exec_command(
            command=f"{command}"
        )[1].read().decode('utf-8').splitlines()


class Statistics:
    def __init__(self, ssh_command_method, args):
        self.command = ssh_command_method
        if args.all:
            args.os = True
            args.ram = True
            args.cpu = True
            args.network = True
            args.users = True
        self.ram if args.ram else None
        self.os if args.os else None
        self.cpu if args.cpu else None
        self.nic if args.network else None
        self.users if args.users else None

    def title(self, title: str):
        print(f"\n{len(title) * '-'}")
        print(f"{title}")
        print(f"{len(title) * '-'}")

    @property
    def ram(self):
        self.title('RAM (in Mo):')
        for line in self.command('free -m'):
            print(line)

    @property
    def os(self):
        self.title('OS Informations:')
        for line in self.command('lsb_release -a'):
            print(line)

    @property
    def cpu(self):
        self.title('CPU Informations:')
        for line in self.command('lscpu'):
            print(line)
        self.title('CPU load:')
        for line in self.command("top -n 1 -b |sed -n '7,15p'"):
            print(line)

    @property
    def nic(self):
        self.title('Network Interface Card Configuration:')
        for line in self.command("cat /etc/netplan/00-installer-config.yaml |sed -n '2,500p'"):
            print(line)
        self.title('Network Stats:')
        for line in self.command("nstat"):
            print(line)

    @property
    def users(self):
        self.title('Users of the system:')
        for line in self.command('cat /etc/passwd'):
            print(f"{self.groups(line.split(':')[0])}")

    def groups(self, user):
        return self.command(f'groups {user}')[0]


if __name__ == '__main__':
    socket = SSH()
    arg = ArgumentParser(
        description="Commands to choose which informations show"
    )
    arg.add_argument('--all', '-a', help="Get all informations from this script", action='store_true')
    arg.add_argument('--ram', '-r', help="Get informations about your RAM (free command)", action='store_true')
    arg.add_argument('--os', '-o', help="Get informations about your OS (lsb_release -a command)", action='store_true')
    arg.add_argument('--cpu', '-c', help="Get informations about your CPU (lscpu command & top)", action='store_true')
    arg.add_argument('--network', '-n', help="Get informations about your NIC (nstat & netplan)", action='store_true')
    arg.add_argument('--users', '-u', help="Get informations about users in the system", action='store_true')
    stats = Statistics(socket.execute_command, arg.parse_args())
    socket.close
