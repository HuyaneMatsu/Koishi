__all__ = ()

from scarletio import LOOP_TIME
from hata import CHANNELS, GUILDS, KOKORO
from hata.ext.solarlink import SolarPlayer

from .constants import LEAVE_TIMEOUT


class Player(SolarPlayer):
    __slots__ = ('__weakref__', 'leave_handle', 'leave_initiated_at',)
    
    def __new__(cls, node, guild_id, channel_id):
        self, waiter = SolarPlayer.__new__(cls, node, guild_id, channel_id)
        self.leave_handle = None
        self.leave_initiated_at = None
        
        return self, waiter
    
    @property
    def queue_duration(self):
        duration = 0.0
        
        for configured_track in self.queue:
            duration += configured_track.track.duration
        
        return duration
    
    
    def check_auto_leave(self, channel_id=0):
        try:
            guild = GUILDS[self.guild_id]
        except KeyError:
            active_users = -999999
        else:
            active_users = 0
            
            if not channel_id:
                channel_id = self.channel_id
            
            for voice_state in guild.voice_states.values():
                if (voice_state.channel_id != channel_id):
                    continue
                
                if voice_state.deaf:
                    continue
                
                if voice_state.self_deaf:
                    continue
                
                if voice_state.user.bot:
                    continue
                
                active_users += 1
        
        if active_users == 0:
            return self.initiate_leave()
        
        self.cancel_leave()
        return False
    
    
    def cancel_leave(self):
        handle = self.leave_handle
        if (handle is not None):
            self.leave_handle = None
            handle.cancel()
        
        self.leave_initiated_at = 0.0
    
    
    def initiate_leave(self):
        now = LOOP_TIME()
        
        handle = self.leave_handle
        if (handle is None):
            self.leave_initiated_at = 0.0
            self.leave_handle = KOKORO.call_at_weak(now+LEAVE_TIMEOUT, self.cancel)
            return True
        
        
        self.leave_initiated_at = now
        return False
    
    
    def cancel(self):
        pass

