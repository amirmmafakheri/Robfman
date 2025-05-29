# roBFMan

**roBFMan** is a flexible command-line tool for fetching and displaying archived content of specific files or pages (like `robots.txt`, `admin.php`, etc.) from multiple domains via [archive.org](https://archive.org/).

---

## Features

- Fetches all available snapshots of any given file or path from archive.org for a domain (or multiple domains).
- Supports single or batch mode for domains and paths.
- Customizable delay between requests.
- Saves output to terminal or to a file.
- MIT License, open for all use cases.

---

## Usage

### Install dependencies

```bash
pip install httpx
```

### Run examples

#### Fetch all archived `robots.txt` for a single domain:

```bash
python robfman.py -t example.com -p robots.txt
```

#### Fetch for multiple domains and multiple paths, with 2 seconds delay, output to file:

```bash
python robfman.py -ft domains.txt -fp paths.txt -d 2 -o output.txt
```

- `domains.txt`: each domain on a separate line (no http/https)
- `paths.txt`: each path or file (like `robots.txt`, `admin.php`) on a separate line

#### All options

| Option | Description |
|--------|-------------|
| `-t, --target` | Single target domain (example: `nobitex.ir`) |
| `-ft, --file_targets` | File with list of domains (one per line) |
| `-p, --path` | Single file/path to fetch (default: `robots.txt`) |
| `-fp, --file_paths` | File with list of paths (one per line) |
| `-d, --delay` | Delay (seconds) between each request (default: 0.5) |
| `-o, --output` | Output file path |

---

## Example `domains.txt`

```
nobitex.ir
digikala.com
example.com
```

## Example `paths.txt`

```
robots.txt
admin.php
wp-login.php
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Project by eMtwo**
