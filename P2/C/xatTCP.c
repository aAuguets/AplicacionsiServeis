#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>

// files descriptors para que lo utilice la funcion select()
static fd_set temporalSet,masterSet;
static int cantidad_fd;

//sockets
static int sock_descriptor, new_socket;
static struct sockaddr_in addr_client, addr_server;
static struct hostent *server;
static socklen_t addrlen;

void init_server(int port){
  FD_ZERO(&masterSet);
  FD_ZERO(&temporalSet);

  //sock descriptor -> Archivo directorio que contiene la conexion de red socket()
  if((sock_descriptor=socket(AF_INET,SOCK_STREAM,0))==-1){
    perror("Error abriendo el socket");
    exit(1);
  }
  bzero((char *) &addr_server, sizeof(addr_server));
  addr_server.sin_family = AF_INET;
  addr_server.sin_addr.s_addr = INADDR_ANY; // Servim/escoltem a qualsevol interficie
  addr_server.sin_port = htons(port); // Convert to network byte order
  //vincula el fd a la @ de avisa al so que se van a conectar a ese puerto
  if (bind(sock_descriptor, (struct sockaddr *) &addr_server, sizeof(addr_server)) < 0) {
    close(sock_descriptor);
    perror("ERROR on binding");
    exit(1);
  }
  listen(sock_descriptor, 5);
  FD_SET(0,&masterSet);//habilitamos para que el server pueda hablar.
  FD_SET(sock_descriptor, &masterSet);
  cantidad_fd = sock_descriptor;
  printf("El  server se ha creadoo bien\n");


}

void init_client(char * IP, int port){
  FD_ZERO(&masterSet);
  FD_ZERO(&temporalSet);
  //se conecta el socket del cliente con el servidor.
  if((sock_descriptor=socket(AF_INET,SOCK_STREAM,0))==-1){
    perror("No se a podido abrir el socket");
    exit(1);
  }
  if((server=gethostbyname(IP))==NULL){
      perror("Error, host no encontrado");
      exit(1);
  }
  bzero((char *)&addr_server,sizeof(addr_server));
  addr_server.sin_family = AF_INET;
  bcopy((char *)server->h_addr,
  (char *)&addr_server.sin_addr.s_addr,
  server->h_length);
  addr_server.sin_port = htons(port);
  if (connect(sock_descriptor, (struct sockaddr *) &addr_server, sizeof(addr_server)) < 0){
    perror("No se a podido abrir el socket");
    exit(1);
  }
  //agregar los fd de stdin + el socket a masterSet
  FD_SET(0,&masterSet);
  FD_SET(sock_descriptor,&masterSet);
  cantidad_fd=sock_descriptor;
  printf("Se ha connectat el client\n");
}

static void add_Connection(void){
  //printf("se ha conectado algo\n");
  addrlen = sizeof addr_client;
  if((new_socket=accept(sock_descriptor,(struct sockaddr *) &addr_client, &addrlen))==-1){
    perror("Error al aceptar");
    exit(1);
  }
  else{
    //agregamos a la lista de conectados
    FD_SET(new_socket,&masterSet);
    if (cantidad_fd < new_socket )
      cantidad_fd= new_socket;
  }
}

static  int del_Connection(int buf, int socket){
  //elimina un FD de la lista y se cierra el socket
  if (buf==0) printf("socket %d se ha ido\n",socket );
  else perror("revc error");
  close(socket);
  FD_CLR(socket,&masterSet);//borramos la conexion
}

static void close_client(void) {
  close(sock_descriptor);
}

static void sendDataToAll(int excludeSocket, char *clientData, int buff) {
  // Enviem les dades a tots els sockets connectats menys a qui ho ha enviat
  int clientSocket;

  for (clientSocket = 0; clientSocket <= cantidad_fd; clientSocket++) {
    if (FD_ISSET(clientSocket, &masterSet) && (clientSocket != sock_descriptor && clientSocket != excludeSocket)) {
      if (send(clientSocket, clientData, buff, 0) == -1) {
	       perror("send error");
      }
    }
    else{
      printf("me llega del teclado del server\n");
    }
  }
}
int main(int argc, char *argv[]){

  char Buffer_client[256];
  int buff; // per el recv
  int socket_client, socket_connected; // per le for()
  char IP_client[INET_ADDRSTRLEN]; //per el send
  int fileDescriptor;

  if ((argc == 3)&&(strcmp(argv[1],"server")==0)){
    int port=atoi(argv[2]);
    init_server(port);
    while (1){
      temporalSet=masterSet;
      bzero(Buffer_client,256);
      //selectClient();

      temporalSet=masterSet;
      if (select(cantidad_fd+1,&temporalSet,NULL,NULL,NULL)==-1){
        perror("Error en Select");
        exit(1);
      }
      for(socket_connected=0;socket_connected<=cantidad_fd;socket_connected++){
        if(FD_ISSET(socket_connected,&temporalSet)){//que FD estan activados
            //si el FD descriptor es el socket del servidor tenemosuna nueva conecion
            //como hago para leer del teclado del server???
          if(socket_connected==sock_descriptor){
            add_Connection();
            printf("(%s | %d) ha entrat al xat, socket num %d\n", inet_ntop(AF_INET, (void *)&((&addr_client)->sin_addr), IP_client, addrlen), addr_client.sin_port, new_socket);
              //  printf("clientes conectados %d\n",cantidad_fd);
          }
          else {//si es algun socket de los cientes(nuevos datos a leer)
            if((buff=recv(socket_connected,Buffer_client,sizeof Buffer_client,0))<=0){
              del_Connection(buff,socket_connected);
            }
            else { //si me llega cualquier otro dato:
              //fgets(Buffer_client,255,stdin);
              printf("newSocket-> %d ha enviado : %s\n",new_socket,Buffer_client);
              
              //sendDataToAll(socket_connected,Buffer_client,buff);
              //tengo que borrar el buffer.
              //envio mesaje a todos:
            }
          }
        }

      }//bucle for()
    }//bucle while()
}
  else if((argc==4)&&(strcmp(argv[1],"client")==0)){
      //ajustes de client
      int port=atoi(argv[3]);
      printf("\tClient %d\n",cantidad_fd);
      init_client(argv[2], port);
      while (1){
        temporalSet=masterSet;
        bzero(Buffer_client,256);
        //selectClient();
        if(select(cantidad_fd+1, &temporalSet,NULL,NULL,NULL)==-1){
          perror("Error en select");
          exit(1);
        }
        //printf("select bien\n");
        for(fileDescriptor=0;fileDescriptor< cantidad_fd;fileDescriptor++){
          //si nos llega algo por el teclado se lo enviamos a todos
        //  if(FD_ISSET(0,&masterSet)){
          if(FD_ISSET(fileDescriptor,&temporalSet)){
            if (fileDescriptor==sock_descriptor){//hemos recibido un mensaje
              if(recv(sock_descriptor,Buffer_client,255,0)<=0){
                close_client();
                printf("el server a tancat\n");
                return 0;
              }
              else {
                printf("\t> %s",Buffer_client);
              }
            }
            else{
              fgets(Buffer_client,255,stdin);
              printf("se ha enviado mensaje\n");
              if(strcmp(Buffer_client,"exit")==0){
                close_client();
                return 0;
              }
              send(sock_descriptor,Buffer_client,strlen(Buffer_client),0);
            //}
            }
          }
        }
      }//final de while del client
    }
    else{
      printf("format incorrecto, se ponde de esta manera\n");
      return 0;
    }
    return 0;
}
