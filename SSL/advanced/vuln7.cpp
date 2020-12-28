// gcc -o build/vuln7 vuln7.cpp
// sample from google project zero.

#include <unistd.h>
#include <stdlib.h>

class IShouldRunCalculator {
public:
    virtual bool UWannaRun() = 0;
};

class CalculatorDecider final : public IShouldRunCalculator {

public:
    CalculatorDecider() : m_run(false) {}

    virtual bool UWannaRun() {
        return m_run;
    }

private:
    bool m_run;

};

class DelegatingCalculatorDecider final : public IShouldRunCalculator {

public:
    DelegatingCalculatorDecider(IShouldRunCalculator *delegate) : m_delegate(delegate) {}

    virtual bool UWannaRun() {
        return m_delegate->UWannaRun();
    }

private:
    IShouldRunCalculator *m_delegate;

};

int main(int argc, const char *argv[]) {
    // Stage 1
    CalculatorDecider nonono;
    DelegatingCalculatorDecider isaidno(&nonono);

    // Stage 2
    IShouldRunCalculator *decider = &isaidno;
    CalculatorDecider *confused_decider = reinterpret_cast<CalculatorDecider *>(decider);

    // Stage 3
    if (confused_decider->UWannaRun())
        system("/bin/sh");
}