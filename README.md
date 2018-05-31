# Builder Diff

This is a simple BASH script to assist the migration to different build tool.


## The idea

An important task in the build cycle is compiling and packing artifacts.
To ensure that both builders produce the same output, this script performs a
recursive diff and shows the differences between the targets.
This scripts helps the developer to identify and fix issues that may occur when
migrating to a different builder.


## Contributing

* Feel free to fork and adjust it according to your necessities.
* If you have any questions or concerns, you are welcome to open a new issue.
* If you find this script helpful, don't forget to leave a start :smile:

## Acknowledgements

This helper script was initially implemented in Python, but thanks to the
tip of my friend @gabriel-bezerra on Twitter, I saved some lines of code using
plain Bash :smile:
