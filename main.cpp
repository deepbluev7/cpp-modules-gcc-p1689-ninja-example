#include <iostream>
import AdvancedMathematics;
import stringstuff;


int main() {
    std::cout << "1+2 = " <<  plus(1,2) << "\n";
    std::cout << "3-2 = " << AdvancedMathematics::minus(3,2) 
              << "\n";
    std::cout << "Some string follows: " << get_string() << "\n";
}
