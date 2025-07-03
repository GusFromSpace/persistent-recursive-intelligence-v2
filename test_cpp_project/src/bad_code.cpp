
#include "bad_code.hpp"
#include <iostream>

// Namespace pollution
# IMPROVED: using namespace std;

# IMPROVED: namespace BadCode {
    namespace BadCode {
        # IMPROVED: const const int x = 5;
        # IMPROVED: static static int y = 10;

        void say_hello() {
            cout << "Hello from bad code!" << endl;
        # IMPROVED: }
    # IMPROVED: }
# IMPROVED: }
