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
    if(link != NULL){
        printf("%d ", link -> element);
        print(link -> next);  
    }
}

node* reverse(node* link){
    if(link -> next == NULL){
        list1 = link;
        return link;
    }
    reverse(link -> next) -> next = link;
    link -> next = NULL;
    return link;
}

int main(){
    for(int i=0;i<8;i++){
        add(i);    
    }
    print(list1);
    std::cout<<std::endl;
    reverse(list1);
    print(list1);
	return 0;
}
