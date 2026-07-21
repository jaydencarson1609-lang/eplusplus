# E++ (English++)

Write code in plain English.

```epp
name is called "Jim"
say "Hello!"
show name
```

**GitHub:** https://github.com/jaydencarson1609-lang/eplusplus

---

## Install

You only need **Python** (free). That’s it.

### Mac

**Step 1 — Get the project**

Open **Terminal** and paste:

```bash
git clone https://github.com/jaydencarson1609-lang/eplusplus.git
cd eplusplus
```

No git? Click the green **Code** button on GitHub → **Download ZIP** → unzip → open the folder in Terminal.

**Step 2 — Try it**

```bash
python3 epp.py example.epp
```

You should see output in the terminal. Done!

**Step 3 — Easy install (optional)**

```bash
chmod +x install.sh
./install.sh
```

This adds colors in VS Code and the `epp` shortcut command.

**Step 4 — VS Code (optional)**

1. Open the `eplusplus` folder in [VS Code](https://code.visualstudio.com/)
2. Open `example.epp`
3. Press **`Cmd+Shift+B`** to run

---

### Windows

**Step 1 — Install Python (one time)**

1. Go to https://www.python.org/downloads/
2. Click **Download Python**
3. Run the installer
4. **Important:** check ✅ **Add python.exe to PATH**
5. Click **Install Now**

**Step 2 — Get the project**

Open **Command Prompt** and paste:

```cmd
git clone https://github.com/jaydencarson1609-lang/eplusplus.git
cd eplusplus
```

No git? Click the green **Code** button on GitHub → **Download ZIP** → unzip → open that folder in Command Prompt.

**Step 3 — Try it**

```cmd
python epp.py example.epp
```

You should see output. Done!

**Step 4 — VS Code (optional)**

1. Open the `eplusplus` folder in [VS Code](https://code.visualstudio.com/)
2. Open `example.epp`
3. Press **`Ctrl+Shift+B`** to run

Double-click **`install.bat`** for a quick setup check.

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
clear screen
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
show 10 modulo 3
show name plus " is cool"
```

### More math (like Lua `math.*`)

```epp
show floor of 3.9
show ceiling of 3.1
show round of 3.6
show absolute of neg
show square root of 16
show remainder of 10 and 3
show power of 2 and 8
show smallest of 10 and 5
show largest of 10 and 5
```

### Text (like Lua `string.*`)

```epp
show length of name
show count of name
show uppercase of name
show lowercase of name
show slice of name from 1 to 3
show find "lo" in hello
show replace "cat" with "dog" in text
show split "a,b,c" by ","
show join parts with "-"
show trimmed of "  hi  "
show copy of "ha" 3 times
when starts with "He" in name then
    say "Yes!"
done
when ends with "!" in msg then
    say "Ends with !"
done
```

### Random

```epp
show choose number between 1 and 10
show pick random item in colors
```

### Type & convert (like Lua `type`, `tonumber`, `tostring`)

```epp
show type of name
show number from "99"
show text from 42
```

### Lists (like Lua `table.*`)

```epp
colors is "red", "blue", "green"
show first item in colors
show last item in colors
show item 2 of colors
add "gold" to colors
remove "red" from colors
remove item 2 from colors
sort colors
reverse colors
show join colors with ", "
when "red" is in colors then
    say "Found red!"
done
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

for i from 1 to 10 do
    say i
done

repeat 100 times
    when score is 10 then
        break loop
    done
done

keep going while lives is greater than 0 do
    say "Still playing!"
done
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

Import with `use "stdlib/math.epp"` etc.

### stdlib/math.epp

| Recipe | Example |
|--------|---------|
| `add` | `show run add with 10 and 5` |
| `subtract` | `show run subtract with 10 and 3` |
| `multiply` | `show run multiply with 4 and 6` |
| `divide` | `show run divide with 20 and 4` |
| `double` | `show run double with 7` |

### stdlib/text.epp

| Recipe | Example |
|--------|---------|
| `make_greeting` | `show run make_greeting with "Jim"` |
| `make_loud` | `show run make_loud with "Wow"` |
| `join_words` | `show run join_words with "Hello" and "world"` |

### stdlib/random.epp

| Recipe | Example |
|--------|---------|
| `coin_flip` | `show run coin_flip` |
| `dice_roll` | `show run dice_roll` |
| `lucky_number` | `show run lucky_number` |

---

## All English words E++ understands

| Idea | Words |
|------|-------|
| Print | `say`, `tell`, `speak`, `print` |
| Show | `show`, `display`, `write` |
| Clear | `clear screen` |
| If | `if`, `when` |
| Else | `else`, `otherwise` |
| End block | `end`, `done`, `finish`, `stop` |
| Variables | `is`, `is called`, `let ... be`, `make ... equal to`, `set ... to` |
| Logic | `and`, `or`, `not` |
| Loops | `repeat`, `while`, `until`, `for each`, `for i from 1 to 10`, `break loop` |
| Functions | `to ... do`, `run ... with`, `give back` |
| Import | `use`, `bring in`, `import`, `share` |
| Objects | `has ... and ...`, `name of player` |
| Lists | `sort`, `reverse`, `remove`, `join ... with`, `add ... to`, `first/last item in` |
| Text | `slice`, `find`, `replace`, `split`, `trimmed`, `copy`, `starts/ends with` |
| Math extra | `floor`, `ceiling`, `round`, `absolute`, `sqrt`, `power`, `modulo`, `min`, `max` |
| Type | `type of`, `number from`, `text from` |
| Random | `choose number between`, `pick random item in` |
| Math | `plus`, `minus`, `times`, `divided by`, `modulo` |
| Compare | `is equal to`, `is not equal to`, `is greater than`, `is less than`, `is in` |
| Input | `ask ... with` |
| Wait | `wait`, `pause` |
| True/false | `yes`, `no`, `true`, `false` |
