from yaml import load

def loadConfigFromFile(filepath):
    """
    Load the configuration options from a filepath

    @param filepath: The filepath to a configuration file.
    @type filepath: C{twisted.python.filepath.FilePath}
    """
    return loadConfigFromString(filepath.getContent())

def loadConfigFromString(s):
    """
    Load the configuration options from a string.

    @param s: a C{str} that contains the yaml formatted
                    configuration
    @type s: yaml formatted C{str}

    @returns: a tuple of hostname and L{engine.ThrottlingDeferred}s
                and the default behavior for unknown urls.
    """
    from turtle import engine

    loaded = load(s)

    # Remove the filtering param
    rest = loaded.pop('filter-rest', True)
    port = loaded.pop('port', 8080)
    # Remove the defaults to use them as
    # a base to work on.
    defaults = loaded.pop('defaults', {})
    # If nothing is in the config file, this is the default
    defaults.update({'calls': 1, 'interval': 1, 'concurrency': 10})

    urlmapping = {}
    for host, kwargs in loaded.iteritems():
        # Fill an empty dictionary with the defaults
        # And then override the defaults with the one
        # in the current block so that we use them
        kw = {}
        kw.update(defaults)
        kw.update(kwargs)
        urlmapping[host] = engine.ThrottlingDeferred(**kw)

    return urlmapping, rest, port

