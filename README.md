# E++ (English++)

**Write code in plain English.** E++ is your own programming language — made for kids, beginners, and anyone who wants coding to feel like talking.

```epp
name is called "Jim"
Age is "14"

say "Hello!"
when Age is greater than 10 then
    say "Jim is a teenager!"
done
```

## Quick start (30 seconds)

```bash
cd ~/Projects/eplusplus
python3 epp.py examples/kids/adventure.epp
python3 epp.py examples/import_demo.epp
```

### New E++ file (example.epp)

In VS Code, with the `eplusplus` folder open:

1. Press **`Cmd+Shift+P`** (Mac) or **`Ctrl+Shift+P`** (Windows)
2. Type **`E++: New example.epp File`** and press Enter
3. It creates `example.epp` (or `example2.epp`, `example3.epp`, …) from a starter template
4. Press **`Cmd+Shift+B`** to run it

New blank tabs also use **E++ colors** automatically (workspace setting).

When you **Save As**, name the file something ending in **`.epp`** — for example `my_game.epp`.

Or install everything (shortcut command + VS Code icon & colors):

```bash
chmod +x install.sh
./install.sh
```

---

## Share E++ with friends

You do **not** need a GitHub **Page** (website). You need a GitHub **repository** (a folder online friends can download).

### Step 1 — Put your project on GitHub

1. Go to [github.com/new](https://github.com/new)
2. Name it something like `eplusplus`
3. Create the repo
4. In Terminal, from your project folder:

```bash
cd ~/Projects/eplusplus
git add .
git commit -m "My E++ language"
git remote add origin https://github.com/YOUR_USERNAME/eplusplus.git
git push -u origin main
```

### Step 2 — Friends install it

Your friends run:

```bash
git clone https://github.com/YOUR_USERNAME/eplusplus.git
cd eplusplus
chmod +x install.sh
./install.sh
```

Then open the folder in VS Code and run any `.epp` file.

### Step 3 — Friends import your scripts

Put shared code in a folder, for example `examples/libs/` or `stdlib/`:

```epp
use "stdlib/math.epp"
bring in "examples/libs/player.epp"
```

If a file is on GitHub inside the repo, the path is the same after they clone it.

To share **your own** recipes, add `share` in the library file:

```epp
share my_helper

to my_helper name do
    give back "Hello " plus name
done
```

### GitHub Page? (optional)

A **GitHub Page** is only if you want a **website** (like a landing page or online docs). It is **not required** for imports or for friends to use E++.

---

## Use E++ in Visual Studio Code

This is the best way to use your language — colored code, snippets, and a **Run** button.

### Step 1 — Open the project

1. Open **Visual Studio Code** (or **Cursor** — same steps)
2. **File → Open Folder…**
3. Choose: `~/Projects/eplusplus`

### Step 2 — Install the E++ extension (one time)

**Easy way** — run the install script (does this for you):

```bash
./install.sh
```

**Manual way** — in a terminal:

```bash
code --install-extension ~/Projects/eplusplus/vscode-extension
```

For Cursor, use `cursor` instead of `code`.

### Step 3 — Open a `.epp` file

1. Open `examples/kids/adventure.epp`
2. You should see:
   - The **E++ icon** on `.epp` files in the file explorer
   - **Colorful syntax** (keywords, strings, comments)
   - Language mode **E++** in the bottom-right corner

### Step 4 — Run your code

Pick any of these:

| Method | How |
|--------|-----|
| **Play button** | Click ▶ in the top-right when a `.epp` file is open |
| **Keyboard** | `Cmd+Shift+B` (Mac) or `Ctrl+Shift+B` (Windows) |
| **Terminal** | `python3 epp.py yourfile.epp` |
| **Command Palette** | `Cmd+Shift+P` → **E++: Run Current File** |

### Step 5 — Use snippets (type & Tab)

In a `.epp` file, type one of these and press **Tab**:

- `say` → print a message
- `let` → make a variable
- `when` → if/else block
- `repeat` → loop
- `ask` → ask the user a question
- `list` → make a list
- `object` → make a JSON-like object
- `to` → create a recipe (function)

---

## Language guide (kid friendly)

### Variables — many English ways

```epp
name is called "Jim"
let age be 14
make score equal to 100
set lives to 3
colors is "red", "blue", "green"
```

### Talk & show

```epp
say "Hello!"
tell "Same thing!"
show name
show score plus 10
```

### Ask the player (input)

```epp
ask name with "What is your name?"
show name
```

### Lists (like JSON `[...]`)

```epp
colors is "red", "blue", "green"
show first item in colors
show last item in colors
show item 2 of colors
```

### Objects (like JSON `{...}`)

```epp
player has name "Jim" and score 100 and alive yes
show name of player
show score of player
```

### If / when

```epp
when age is greater than 10 then
    say "Big kid!"
otherwise
    say "Little kid!"
done
```

Also works: `if ... then ... else ... end`

### Loops

```epp
repeat 5 times
    say "Fun!"
done

while score is less than 100 do
    make score equal to score plus 10
done

for each color in colors do
    say color
done
```

### Recipes (functions)

```epp
to greet someone do
    say "Hello " plus someone
done

run greet with "Jim"
```

### Math

```epp
show 10 plus 5
show 20 minus 3
show 4 times 6
show 10 divided by 2
```

### Compare

```epp
when age is equal to 14 then
    say "Exactly 14!"
done

when name is not equal to "Bob" then
    say "Not Bob!"
done
```

### Recipes (functions) with return values

```epp
to add a and b do
    give back a plus b
done

show run add with 10 and 5
```

### Import other scripts (build your language library)

```epp
use "stdlib/math.epp"
bring in "examples/libs/player.epp"

show run add with 10 and 5
show run make_greeting with "Jim"
```

Ways to import:

| English | Meaning |
|---------|---------|
| `use "file.epp"` | Load another script |
| `bring in "file.epp"` | Same thing, natural English |
| `import "file.epp"` | Same thing |
| `use script from "file.epp"` | Same thing, extra English |

In the file you import, mark what to share:

```epp
share add and make_greeting

to add a and b do
    give back a plus b
done
```

If you skip `share`, everything in that file becomes available.

Built-in library (in `stdlib/`):

- `stdlib/math.epp` — add, subtract, multiply, divide, double
- `stdlib/text.epp` — make_greeting, make_loud, join_words

### Wait

```epp
wait 2 seconds
```

### Yes / No (true / false)

```epp
let ready be yes
when ready is no then
    say "Not yet!"
done
```

---

## All the English words E++ understands

| Idea | Words you can use |
|------|-------------------|
| Print | `say`, `tell`, `speak`, `print` |
| Show value | `show`, `display` |
| If | `if`, `when` |
| Else | `else`, `otherwise` |
| End block | `end`, `done`, `finish` |
| Set variable | `is`, `is called`, `let ... be`, `make ... equal to`, `set ... to` |
| And / Or | `and`, `or`, `not` |
| Loop | `repeat`, `while`, `until`, `for each` |
| Function | `to ... do`, `run ... with`, `give back` |
| Import | `use`, `bring in`, `import`, `share` |
| Object | `has ... and ...` |
| List item | `first item in`, `last item in`, `item 2 of` |

---

## Project layout

```
eplusplus/
  eplusplus/           # language engine
  epp.py               # run scripts
  install.sh           # one-click setup
  vscode-extension/    # VS Code icon, colors, snippets, play button
  examples/kids/       # fun starter scripts
  examples/libs/       # your own importable libraries
  stdlib/              # built-in E++ modules
```

---

## What's next?

This is **your** language — v0.3. Ideas to add later:

- Web version (run in browser)
- Draw graphics (`draw a red circle`)
- More stdlib modules (games, colors, random)
- More JSON helpers

Made with E++ — English++ 🚀
