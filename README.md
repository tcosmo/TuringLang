# `alang`: Turing machines specification language and simulator

`alang` allow you to write and simulate Turing machine. It comes with a GUI, `alangui` which allows you to visualise
your machines' executions.

Machines are specified in a [YAML](https://en.wikipedia.org/wiki/YAML)-based language, see for instance:

- `example_machines/copy.yaml`: A machine that copies the content of its input tape on its output tape
- `example_machines/parity.yaml`: A machine that computes the parity of the number of `1`s in a binary input
- `example_machines/palindrome.yaml`: A machine that decides if its binary input is a palindrome or not
- `example_machines/binary_adder.yaml`: A machine that adds two inputs in binary

## Get started

`alang` has been tested on `python3.6`, `python3.7`, `python3.8`, `python3.9`.
To get started with `alang` you need

```bash
git clone https://github.com/tcosmo/alang.git
cd alang
virtualenv venv --python=/usr/bin/python3.{6,7,8,9}
source venv/bin/activate
pip install -r requirements.txt
```

Then you can for instance run machines in the gui (press `n` to run one machine step), for instance:

- `python run_gui.py example_machines/copy.yaml 1100011`
- `python run_gui.py example_machines/copy.yaml 1100011`
- `python run_gui.py example_machines/parity.yaml 100010`
- `python run_gui.py example_machines/parity.yaml 1011`
- `python run_gui.py example_machines/palindrome.yaml 1100010`
- `python run_gui.py example_machines/palindrome.yaml 1100011`
- `python run_gui.py example_machines/binary_adder.yaml 001 001`
- `python run_gui.py example_machines/binary_adder.yaml 0011111 1011`