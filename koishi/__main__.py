__all__ = ()

from .cli import main

if __name__ == '__main__':
    main()

else:
    # Import things depending on settings and which file is started up.
    #
    # As self host, turn `RUN_WEBAPP_AS_MAIN` on and run this file.
    #
    # If hosting, wsgi will import this file, so the bots will not start up. Those need to be started up separately by an
    # always running task.
    
    try:
        from hata import KOKORO
    except ImportError:
        pass
    else:
        KOKORO.stop()
    
    from .web import WEBAPP
