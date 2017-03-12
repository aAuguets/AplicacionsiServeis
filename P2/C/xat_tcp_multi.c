#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <netinet/in.h>
//#include <netdb.h>
//#include <arpa/inet.h>

#define  PORT 10000

static fd_set fd_descriptor;
static int cantidad_fd;

static int sock_descriptor, new_socket_client;
static struct sockaddr_in addr_client, addr_server;
static struct hostent *server;
static int lista_clientes[4];//max de clientes
static socklen_t addrlen;
static int punter;
static char buffer_server[256];
static char buffer_client[256];
static int buff;

static void sendDataToAll(int excludeSocket, char *clientData, int buff) {
  // Enviem les dades a tots els sockets connectats menys a qui ho ha enviat
  int clientSocket;
  for (clientSocket = 0; clientSocket <=lista_clientes[clientSocket] ; clientSocket++) {
    if (FD_ISSET(clientSocket, &fd_descriptor) && (clientSocket != sock_descriptor && clientSocket != excludeSocket)) {
      if (send(clientSocket, clientData, buff, 0) == -1) {
	       perror("send error");
      }
    }
  }
}

int main(void){
  int clientac=0;

  if(sock_descriptor=socket(AF_INET,SOCK_STREAM,0)==-1){
    perror("Error abriendo el socket");
    exit(1);
  }
  printf("socket abierto...\n preparado para escuchar a los clientes");
  bzero((char *) &addr_server, sizeof(addr_server));
  addr_server.sin_family = AF_INET;
  addr_server.sin_addr.s_addr = INADDR_ANY; // Servim/escoltem a qualsevol interficie
  addr_server.sin_port = htons(PORT);
  if(bind(sock_descriptor, (struct sockaddr *) &addr_server, sizeof(addr_server)) < 0) {
    close(sock_descriptor);
    perror("ERROR on binding");
    exit(1);
    return 0;
  }
  printf("caca");
  listen(sock_descriptor, 5);
  //hast aqui creamos el server
  while (1){
    FD_ZERO(&fd_descriptor);
    FD_SET(0,&fd_descriptor);//este es el teclado
    FD_SET(sock_descriptor,&fd_descriptor);//este es el teclado
    for(int i=0;i<clientac;i++){
      FD_SET(lista_clientes[i],&fd_descriptor);
    }
    if ((new_socket_client=select(FD_SETSIZE,&fd_descriptor,NULL,NULL,NULL))==-1){
      perror("Error en Select");
      exit(1);
    }
    if(FD_ISSET(new_socket_client,&fd_descriptor)){
      //printf("(%s | %d) ha entrat al xat, socket num %d\n", inet_ntop(AF_INET, (void *)&((&addr_client)->sin_addr), IP_client, addrlen), addr_client.sin_port, new_socket);
      printf("conexxion entrante %d",clientac);
      addrlen = sizeof addr_client;
      if((new_socket_client=accept(sock_descriptor,(struct sockaddr *) &addr_client, &addrlen))==-1){
        perror("Error al aceptar");
        exit(1);
      }
      lista_clientes[clientac++]=new_socket_client;
    }
    if(FD_ISSET(0,&fd_descriptor)){
      fgets(buffer_server,255,stdin);
      sendDataToAll(0,buffer_server,buff);
      bzero(buffer_server,256);
    }
    else{
      for (punter=0;punter < clientac;punter++){
        if(FD_ISSET(lista_clientes[punter],&fd_descriptor)){
          bzero(buffer_client,255);
          if(buff=read(lista_clientes[punter],buffer_client,255)<=0){
            printf("el socket %d se ha ido\n",punter);
            close(punter);
            FD_CLR(punter,&fd_descriptor);
          }
          else{
          printf("cliente %d, : %s",punter,buffer_client);
          }
          bzero(buffer_client,256);
        }
      }
    }
  }
}
