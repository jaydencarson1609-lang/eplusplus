# E++ (English++)

Write code in plain English.

```epp
name is called "Jim"
Age is "14"
say "Hello!"
show name
```

---

## Install

### 1. Download

```bash
git clone https://github.com/jaydencarson1609-lang/eplusplus.git
cd eplusplus
```

### 2. Install (one time)

```bash
chmod +x install.sh
./install.sh
```

This adds the `epp` command and the VS Code extension (colors, snippets, run button).

### 3. Run a script

```bash
python3 epp.py example.epp
```

Or with the shortcut:

```bash
epp example.epp
```

### 4. VS Code (optional)

1. Open the `eplusplus` folder in VS Code
2. Open any `.epp` file
3. Press **`Cmd+Shift+B`** (Mac) or **`Ctrl+Shift+B`** (Windows) to run
4. Or press **`Cmd+Shift+P`** → **E++: New example.epp File** to start a new script

---

## All functions

### Variables

```epp
name is called "Jim"
let age be 14
make score equal to 100
set lives to 3
colors is "red", "blue", "green"
```

### Print

```epp
say "Hello!"
tell "Hello!"
show name
show score plus 10
```

### Input

```epp
ask name with "What is your name?"
```

### Math

```epp
show 10 plus 5
show 20 minus 3
show 4 times 6
show 10 divided by 2
show name plus " is cool"
```

### Compare

```epp
when age is equal to 14 then
    say "Exactly 14!"
done

when age is not equal to 10 then
    say "Not 10!"
done

when age is greater than 10 then
    say "Big!"
done

when age is less than 20 then
    say "Small!"
done

when ready is yes and score is greater than 0 then
    say "Go!"
done
```

### If / else

```epp
when age is greater than 10 then
    say "Big kid!"
otherwise
    say "Little kid!"
done
```

Also works: `if ... then ... else ... end` / `done`

### Loops

```epp
repeat 5 times
    say "Fun!"
done

while score is less than 100 do
    make score equal to score plus 10
done

until score is greater than 99 do
    make score equal to score plus 10
done

for each color in colors do
    say color
done

keep going while lives is greater than 0 do
    say "Still playing!"
done
```

### Lists

```epp
colors is "red", "blue", "green"
show first item in colors
show last item in colors
show item 2 of colors
```

### Objects

```epp
player has name "Jim" and score 100 and alive yes
show name of player
show score of player
```

### Recipes (functions)

```epp
to greet someone do
    say "Hello " plus someone
done

run greet with "Jim"
```

Return a value:

```epp
to add a and b do
    give back a plus b
done

show run add with 10 and 5
```

### Import

```epp
use "stdlib/math.epp"
import "myfile.epp"
bring in "myfile.epp"
use script from "myfile.epp"

share add and make_greeting

to add a and b do
    give back a plus b
done
```

### Wait

```epp
wait 2 seconds
wait 1 minute
```

### Comments

```epp
# line comment
note: this is also a comment
```

### Yes / no

```epp
let ready be yes
when ready is no then
    say "Not yet!"
done
```

---

## Built-in library (stdlib)

Import with `use "stdlib/math.epp"` or `use "stdlib/text.epp"`.

### stdlib/math.epp

| Recipe | What it does | Example |
|--------|--------------|---------|
| `add` | Add two numbers | `show run add with 10 and 5` |
| `subtract` | Subtract | `show run subtract with 10 and 3` |
| `multiply` | Multiply | `show run multiply with 4 and 6` |
| `divide` | Divide | `show run divide with 20 and 4` |
| `double` | Double a number | `show run double with 7` |

### stdlib/text.epp

| Recipe | What it does | Example |
|--------|--------------|---------|
| `make_greeting` | Hello message | `show run make_greeting with "Jim"` |
| `make_loud` | Adds `!!!` | `show run make_loud with "Wow"` |
| `join_words` | Join with a space | `show run join_words with "Hello" and "world"` |

---

## All English words E++ understands

| Idea | Words |
|------|-------|
| Print | `say`, `tell`, `speak`, `print` |
| Show | `show`, `display`, `write` |
| If | `if`, `when` |
| Else | `else`, `otherwise` |
| End block | `end`, `done`, `finish`, `stop` |
| Variables | `is`, `is called`, `let ... be`, `make ... equal to`, `set ... to` |
| Logic | `and`, `or`, `not` |
| Loops | `repeat`, `while`, `until`, `for each`, `keep going while` |
| Functions | `to ... do`, `run ... with`, `give back` |
| Import | `use`, `bring in`, `import`, `share` |
| Objects | `has ... and ...`, `name of player` |
| Lists | `first item in`, `last item in`, `item 2 of` |
| Math | `plus`, `minus`, `times`, `divided by` |
| Compare | `is equal to`, `is not equal to`, `is greater than`, `is less than` |
| Input | `ask ... with` |
| Wait | `wait`, `pause` |
| True/false | `yes`, `no`, `true`, `false` |
