#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>

int main(){
    int fd = open("/challenge/vault", O_RDONLY);
    sleep(10);
    char buf[256];
    read(fd, buf, 256);
    printf(buf);
    return 0;
}