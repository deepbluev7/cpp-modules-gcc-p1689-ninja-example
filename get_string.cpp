module;

#include <string>

#define STRINGSTUFF stringstuff

export module STRINGSTUFF ;

export std::string get_string() {
    return "abc";
}
