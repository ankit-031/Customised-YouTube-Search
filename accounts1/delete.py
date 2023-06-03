from accounts.models import Playlist

# Delete all playlists with a view_count less than 1000
Playlist.objects.filter(view_count__lt=1000).delete()
