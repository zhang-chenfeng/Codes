#include <iostream>

struct node{
	int element;
	node* next;
};
struct node* list1 = NULL;

void add(int x){
	node* n = new node;
	n -> element = x;
	n -> next = list1;
	list1 = n;
}

void print(node* link){
    if(link != nullptr){
        printf("%d ", link -> element);
        print(link -> next);  
    }
}

void reverse(node* link){
    if(link -> next == nullptr){
        list1 = link;
    }
    link -> next -> next = link;
    link -> next = nullptr;
}

int main(){
    for(int i=0;i<8;i++){
        add(i);    
    }
    print(list1);
    printf("\n");
    reverse(list1);
    print(list1);
	return 0;
}
