import java.io.*;
import java.util.*;
import java.lang.Character;

public class Main {
  static void add(Stack<Integer> st1, Stack<Integer> st2, boolean qw){
    Stack<Integer> c = new Stack<>();
    int carry = 0;
    int sum = 0;
    while(!st1.isEmpty() || !st2.isEmpty()){
      if(st1.isEmpty()){
        sum = st2.pop() + carry;
        carry = 0;
      } else if(st2.isEmpty()){
        sum = st1.pop() + carry;
        carry = 0;
      } else {
        sum = st1.pop() + st2.pop() + carry;
        carry = sum/10;
        sum = sum%10;
      }
      c.push(sum);
    }
    if(carry >0){
      c.push(carry);
    }
    if(qw){
      System.out.print("-");
    }
    while(!c.isEmpty()){
      System.out.print(c.pop());
    }
  }
  
  static void subtract(Stack<Integer> st1, Stack<Integer> st2, boolean ssd){
    Stack<Integer> fin = new Stack<>();
    if(ssd){
      System.out.print("-");
    }
    int carry = 0;
    int num1;
    int num2;
    int diff;
    boolean tr = false;
    while(!st1.isEmpty()){
      num1 = st1.pop() + carry;
      if(st2.isEmpty()){
        num2 = 0;
      } else {
        num2 = st2.pop();
      }
      diff = num1 - num2;
      if(diff<0){
        diff = diff + 10;
        carry = -1;
      } else {
        carry = 0;
      }
      fin.push(diff);
    }
    while(!fin.isEmpty()){
      num2 = fin.pop();
      if(!tr&&num2==0){
        continue;
      } else {
        System.out.print(num2);
        tr = true;
      }
    }
  }

  public static void main(String[] args) {
    Scanner iuyg = new Scanner(System.in);
    int c = iuyg.nextInt();
    for(int x =0;x<c;x++){
      boolean aneg = false;
      boolean bneg = false;
      String num1 = iuyg.next();
      String num2 = iuyg.next();
      if (num1.substring(0, 1).equals("-")){
        aneg = true;
        num1 = num1.substring(1);
      }
      if (num2.substring(0, 1).equals("-")){
        bneg = true;
        num2 = num2.substring(1);
      }
      Stack<Integer> la = new Stack<>();
      Stack<Integer> lb = new Stack<>();
      for(int y = 0;y<num1.length();y++){
        la.push(Character.getNumericValue(num1.charAt(y)));
      }
      for(int z = 0;z<num2.length();z++){
        lb.push(Character.getNumericValue(num2.charAt(z)));
      }
      if(aneg == bneg){
        add(la, lb, aneg);
      } else {
        if(num1.length() > num2.length()){
          subtract(la, lb, aneg);
        } else if(num2.length() > num1.length()){
          subtract(lb, la, bneg);
        } else {
          for(int u = 0; u<num1.length();u++){
            int qqq = Character.getNumericValue(num1.charAt(u));
            int www = Character.getNumericValue(num2.charAt(u));
            if(qqq>www){
              subtract(la, lb, aneg);
              break;
            } else if(www>qqq) {
              subtract(lb, la, bneg);
              break;
            } else if(u == num1.length() -1){
              System.out.print(0);
              break;
            }
          }
        }
      }
      System.out.println();
    }
  }
}
