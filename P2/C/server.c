/* A simple server in the internet domain using TCP
   The port number is passed as an argument */
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>

void error(const char *msg)
{
    perror(msg);
    exit(1);
}

int main(int argc, char *argv[])
{
     int sockfd, newsockfd, portno;
     socklen_t clilen;
     char buffer[256];
     struct sockaddr_in serv_addr, cli_addr;
     int n;
     if (argc < 2) {
         fprintf(stderr,"ERROR, no port provided\n");
         exit(1);
     }

     sockfd = socket(AF_INET, SOCK_STREAM, 0);
     if (sockfd < 0) 
        error("ERROR opening socket");
    //llena el buffer de 0
     bzero((char *) &serv_addr, sizeof(serv_addr));
     portno = atoi(argv[1]);
     serv_addr.sin_family = AF_INET;
     //contiene la direccion ip del host.
     //siempre sera la direccion de la maquina donde esta corriendo el programa
     serv_addr.sin_addr.s_addr = INADDR_ANY;
     //es importante para convertir el numero del puerto en un host a nivel de byte
     //htons()-> mirar
     serv_addr.sin_port = htons(portno);
     if (bind(sockfd, (struct sockaddr *) &serv_addr,sizeof(serv_addr)) < 0) 
        error("ERROR on binding");
    listen(sockfd,5);
    clilen = sizeof(cli_addr);
    while (1) {
        if( newsockfd = accept(sockfd,(struct sockaddr *) &cli_addr,&clilen)==-1){
            perror("accept");
            exit(1);
        }
        printf("Se ha conectat un nou socket\n");
        /*if (newsockfd < 0) 
            error("ERROR on accept");*/
        //bzero(buffer,256);
        n = read(newsockfd,buffer,255);
        //while(1){
            //n = read(newsockfd,buffer,255);
            if (n < 0) error("ERROR reading from socket");
            printf("Here is the message: %s\n",buffer);
            if(n = write(newsockfd,&buffer,18)== -1){
                error("ERROR writing to socket");
                close(newsockfd);
            }
            printf("\nServer ha enviado mensaje\n");
            n = read(newsockfd,buffer,255);
        //}
    }
    close(sockfd);
    return 0; 
}

