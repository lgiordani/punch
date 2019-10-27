## The punch workflow

The way punch works can be summarized by the following workflow:

1. The config file and the version file are read from the disk
2. The current version is built according to the configuration of the parts (from the config file) and their actual values (from the version file)
3. The new version is created incrementing the part requested by the user and changing the rest of the version accordingly
4. Each file listed in the configuration file is opened, processed by each of the global or local serializers, replacing the old version with the new one
5. The new version is written into the version file
6. The VCS requested actions are executed

