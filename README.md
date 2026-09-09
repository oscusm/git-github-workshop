# Git & GitHub Workshop

Welcome! By the end of this workshop you will have:

- forked a repository
- made a branch
- committed a change
- pushed it to GitHub
- opened a pull request that gets merged

...and your name will show up on the live site:

**https://oscusm.github.io/git-github-workshop/**

Everything you need is on this page. Every command is copy-pasteable.

If you get stuck at any step, jump to [Troubleshooting](#7-troubleshooting) or
raise your hand.

---

## What you are going to add

One file, named after your GitHub username, in the `people/` folder:

```
people/<your-github-username>.md
```

That's it. One file. Nothing else.

---

## 1. Fork this repo

A **fork** is your own copy of somebody else's repo, living under your GitHub
account. You can do whatever you want in your fork without touching the original.

1. Go to <https://github.com/oscusm/git-github-workshop>
2. Click the **Fork** button (top right).
3. Leave every setting as-is and click **Create fork**.

**Check that it worked.** Look at the URL bar. It should now say **your**
username, not `oscusm`:

```
https://github.com/YOUR-USERNAME/git-github-workshop
```

If it still says `oscusm/git-github-workshop`, you are looking at the original
repo and the fork did not happen. Go back and click Fork again.

---

## 2. Clone your fork

**Cloning** downloads your fork onto your laptop.

### Option A — command line

On **your fork's** page, click the green **Code** button and copy the URL. Then:

```bash
git clone https://github.com/YOUR-USERNAME/git-github-workshop.git
```

```bash
cd git-github-workshop
```

That `cd` matters. Every command after this one has to run *inside* the project
folder. If you skip it, git will tell you `not a git repository`.

Confirm you are in the right place:

```bash
git status
```

You should see `On branch main` and `nothing to commit, working tree clean`.

### Option B — GitHub Desktop

1. On **your fork's** page, click **Code** → **Open with GitHub Desktop**.
2. GitHub Desktop opens and asks where to put the folder. Pick anywhere and
   click **Clone**.
3. If it asks "How are you planning to use this fork?", choose
   **To contribute to the parent project**.

To follow along with the terminal commands from inside GitHub Desktop, use
**Repository → Open in Terminal** (or Command Prompt on Windows).

---

## 3. Create a branch

A **branch** is a separate line of work. You make your changes on a branch so
that `main` stays clean.

```bash
git switch -c add-YOURUSERNAME
```

Replace `YOURUSERNAME` with your actual GitHub username. So if your username is
`golden-eagle`, you run:

```bash
git switch -c add-golden-eagle
```

`-c` means "create it". You are now on that branch. Check with:

```bash
git status
```

It should say `On branch add-YOURUSERNAME`.

**GitHub Desktop:** click the **Current Branch** dropdown at the top →
**New Branch** → type `add-YOURUSERNAME` → **Create Branch**.

---

## 4. Create your file

Create a file at `people/YOURUSERNAME.md`. The **filename must be your GitHub
username** — that is how the site links your card to your profile.

The format is two parts: a heading line with your display name, then a fun fact.

```markdown
# Your Display Name
A fun fact about you. One or two sentences is perfect.
```

A real example. If your username is `golden-eagle`, the file
`people/golden-eagle.md` might look like:

```markdown
# Sam Rivera
I have visited 14 national parks and I can solve a Rubik's cube in under two
minutes, but I still cannot parallel park.
```

Keep it friendly — it goes on a public website that will be projected on a
screen.

### Making the file

Use your editor (VS Code: **File → New File**, save it in the `people` folder),
or do it from the terminal:

```bash
cat > people/YOURUSERNAME.md <<'END'
# Your Display Name
A fun fact about you goes right here.
END
```

Check that git noticed it:

```bash
git status
```

You should see your file listed in red under **Untracked files**.

---

## 5. Commit and push

**Commit** = save a snapshot with a message. **Push** = upload it to GitHub.

Stage your file:

```bash
git add people/YOURUSERNAME.md
```

Commit it with a message:

```bash
git commit -m "Add YOURUSERNAME to people"
```

Push the branch to your fork:

```bash
git push -u origin add-YOURUSERNAME
```

`-u origin add-YOURUSERNAME` means "send this branch to my fork on GitHub and
remember it", so next time `git push` alone is enough.

**GitHub Desktop:** your change appears in the left panel. Type a summary in the
**Summary** box at the bottom left, click **Commit to add-YOURUSERNAME**, then
click **Publish branch** at the top.

---

## 6. Open a pull request

A **pull request (PR)** asks the original repo to take your change.

1. Go to your fork on GitHub. There will be a yellow banner:
   **"add-YOURUSERNAME had recent pushes"** → click **Compare & pull request**.
   (No banner? Click the **Pull requests** tab → **New pull request**.)
2. **Read the two dropdowns at the top of the page carefully:**

   ```
   base repository: oscusm/git-github-workshop    base: main
   head repository: YOUR-USERNAME/git-github-workshop    compare: add-YOURUSERNAME
   ```

   The **base repository must be `oscusm/git-github-workshop`** — the original,
   not your fork. If both sides say your username, click the base repository
   dropdown and pick `oscusm/git-github-workshop`. A PR from your fork into your
   own fork does nothing.
3. Give it a title like `Add Sam Rivera` and click **Create pull request**.

Done. We merge it live, the site rebuilds in about a minute, and your name
appears at <https://oscusm.github.io/git-github-workshop/>.

**GitHub Desktop:** after publishing your branch, click
**Create Pull Request** — it opens the browser on the PR page. Still check the
base repository dropdown.

---

## 7. Troubleshooting

### Push failed: authentication / "Support for password authentication was removed"

GitHub does not accept your account password over the command line.

**Easiest fix — use GitHub Desktop.** Sign in with
**File → Options → Accounts → Sign in** (macOS: **GitHub Desktop → Settings**),
then push from there. It handles the credentials for you.

**Command-line fix — use a Personal Access Token (PAT)** as your password:

1. Go to <https://github.com/settings/tokens> →
   **Generate new token (classic)**.
2. Name it `workshop`, set expiration to 7 days, check the **`repo`** box.
3. Click **Generate token** and copy it. You will not see it again.
4. Run `git push` again. For **username** enter your GitHub username; for
   **password** paste the token.

Nothing appears while you paste the token — that is normal, just press Enter.

### "nothing to commit, working tree clean"

Git sees no changes. Usually one of:

- You never saved the file in your editor. Save it (`Ctrl+S` / `Cmd+S`).
- You created the file somewhere else. Check you are in the right folder:
  ```bash
  pwd
  ls people/
  ```
  Your file should be in that list.
- You forgot `git add`:
  ```bash
  git add people/YOURUSERNAME.md
  ```

### I committed to `main` instead of my branch

No problem. Make the branch from where you are — it carries your commit with it:

```bash
git switch -c add-YOURUSERNAME
```

```bash
git push -u origin add-YOURUSERNAME
```

Then put your local `main` back to normal:

```bash
git switch main
```

```bash
git reset --hard origin/main
```

`reset --hard` throws away local changes on `main`. That is what you want here —
your work is safe on the other branch.

### I pushed to the wrong branch name

Push again under the right name, and delete the wrong one from GitHub:

```bash
git push -u origin add-YOURUSERNAME
```

```bash
git push origin --delete wrong-branch-name
```

### "fatal: not a git repository"

You are outside the project folder. You forgot to `cd`:

```bash
cd git-github-workshop
```

```bash
git status
```

Still lost? Find it:

```bash
cd ~
```

```bash
find . -name git-github-workshop -maxdepth 4 -type d
```

### My PR shows dozens of changed files

Your fork is out of date with the original. Refresh it:

```bash
git remote add upstream https://github.com/oscusm/git-github-workshop.git
```

```bash
git fetch upstream
```

```bash
git switch main
```

```bash
git reset --hard upstream/main
```

Then redo your branch from step 3.

---

## 8. Undoing things

Everybody breaks something. Here is how to unbreak it.

### `git restore` — throw away edits you have not committed

You edited a file, hate it, and want the last committed version back.

```bash
git restore people/YOURUSERNAME.md
```

Whole folder at once:

```bash
git restore .
```

There is no undo for this one — the edits are gone.

**GitHub Desktop:** right-click the file in the **Changes** list →
**Discard changes**.

### `git reset --soft HEAD~1` — undo the last commit, keep the work

You committed too early, or with a bad message. This removes the commit but
leaves your files exactly as they are, staged and ready to commit again.

```bash
git reset --soft HEAD~1
```

```bash
git commit -m "A better message this time"
```

Only use this on commits you have **not pushed** yet.

**GitHub Desktop:** **History** tab → right-click the top commit →
**Undo commit**.

### `git revert <sha>` — undo a commit that is already pushed

Once a commit is on GitHub and other people have it, don't rewrite history.
Instead, make a *new* commit that reverses the old one.

Find the commit ID:

```bash
git log --oneline
```

Revert it (use the short ID from the first column):

```bash
git revert a1b2c3d
```

An editor opens with a prepared message — save and close it. Then push:

```bash
git push
```

**GitHub Desktop:** **History** tab → right-click the commit →
**Revert changes in commit**, then **Push origin**.

### Which one do I want?

| Situation | Command |
| --- | --- |
| Bad edits, not committed | `git restore <file>` |
| Bad commit, not pushed | `git reset --soft HEAD~1` |
| Bad commit, already pushed | `git revert <sha>` |

---

## For maintainers

Build the site locally (Python 3.11+, standard library only — nothing to
install):

```bash
python3 build.py
```

```bash
python3 -m http.server -d _site 8000
```

Then open <http://localhost:8000>.

- `build.py` reads `people/*.md`, skips files starting with `_`, escapes all
  user content, and writes `_site/`.
- A malformed participant file is skipped with a warning instead of failing the
  build, so one bad PR can never take the site down.
- `.github/workflows/deploy.yml` rebuilds and deploys on every push to `main`,
  and can be run by hand from the **Actions** tab (**Run workflow**).
- Repo setting to check once: **Settings → Pages → Source → GitHub Actions**.
