__all__ = ('WaifuType', )

from scarletio import RichAttributeErrorBaseType, Task
from hata import KOKORO
from hata.ext.extension_loader import import_extension

get_default_user_stats = import_extension('.constants', 'get_default_user_stats')

from bot_utils.models import DB_ENGINE, WAIFU_STATS_TABLE, waifu_stats_model


ENTRY_ID_INITIALIZING = -2
ENTRY_ID_NON_EXISTENT = -1

SAVING_STATE_NONE = 0
SAVING_STATE_SAVING = 1
SAVING_STATE_RE_SAVE = 2


class WaifuType(RichAttributeErrorBaseType):
    __slots__ = (
        'user_id', 'entry_id', 'stat_housewife', 'stat_cuteness', 'stat_bedroom', 'stat_charm', 'stat_loyalty',
        'level', 'experience', 'raw_species', 'raw_weapon', 'raw_costume', 'saving_state'
    )
    
    def __new__(cls, user):
        self = object.__new__(cls)
        self.user_id = user.id
        self.saving_state = SAVING_STATE_NONE
        
        self.entry_id = ENTRY_ID_INITIALIZING
        
        self.stat_housewife = 0
        self.stat_cuteness = 0
        self.stat_bedroom = 0
        self.stat_charm = 0
        self.stat_loyalty = 0
        
        self.level = 0
        self.experience = 0
        
        self.raw_species = 0
        self.raw_weapon = 0
        self.raw_costume = 0
        
        return self
    
    def __await__(self):
        entry_id = self.entry_id
        
        if entry_id == ENTRY_ID_INITIALIZING:
            yield from self._load_from_database().__await__()
        
        return self
    
    
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' user_id=')
        repr_parts.append(repr(self.user_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    # In generators we cannot use async context managers, so we define async function, and use yield from `.__await__()`
    # instead
    
    if (DB_ENGINE is None):
        async def _load_from_database(self):
            self.entry_id = ENTRY_ID_NON_EXISTENT
            self.stat_housewife, self.stat_cuteness, self.stat_bedroom, self.stat_charm, self.stat_loyalty = \
                get_default_user_stats(self.user_id)
    
    else:
        async def _load_from_database(self):
            async with DB_ENGINE.connect() as connector:
                response = await connector.execute(
                    WAIFU_STATS_TABLE.select(
                        waifu_stats_model.user_id == self.user_id,
                    )
                )
                
                result = await response.fetchone()
            
            if result is None:
                self.entry_id = ENTRY_ID_NON_EXISTENT
                self.stat_housewife, self.stat_cuteness, self.stat_bedroom, self.stat_charm, self.stat_loyalty = \
                    get_default_user_stats(self.user_id)
            
            else:
                self.entry_id = result.id
                
                self.stat_housewife = result.stat_housewife
                self.stat_cuteness = result.stat_cuteness
                self.stat_bedroom = result.stat_bedroom
                self.stat_charm = result.stat_charm
                self.stat_loyalty = result.stat_loyalty
                
                self.level = result.level
                self.experience = result.experience
                
                self.raw_species = result.raw_species
                self.raw_weapon = result.raw_weapon
                self.raw_costume = result.raw_costume
    
    
    if (DB_ENGINE is None):
        def save(self):
            pass
    
    else:
        def save(self):
            saving_state = self.saving_state
            if (saving_state == SAVING_STATE_NONE):
                Task(self._save_task(), KOKORO)
                self.saving_state = SAVING_STATE_SAVING
                
            elif (saving_state == SAVING_STATE_SAVING):
                self.saving_state = SAVING_STATE_RE_SAVE
        
        
        async def _save_task(self):
            try:
                async with DB_ENGINE.connect() as connector:
                    while True:
                        entry_id = self.entry_id
                        if entry_id == ENTRY_ID_NON_EXISTENT:
                            response = await connector.execute(
                                WAIFU_STATS_TABLE.insert().values(
                                    user_id = self.user_id,
                                    
                                    stat_housewife = self.stat_housewife,
                                    stat_cuteness = self.stat_cuteness,
                                    stat_bedroom = self.stat_bedroom,
                                    stat_charm = self.stat_charm,
                                    stat_loyalty = self.stat_loyalty,
                                    
                                    level = self.level,
                                    experience = self.experience,
                                    
                                    raw_species = self.raw_species,
                                    raw_weapon = self.raw_weapon,
                                    raw_costume = self.raw_costume,
                                ).returning(
                                    waifu_stats_model.id,
                                )
                            )
                            
                            result = await response.fetchone()
                            entry_id = result[0]
                            self.entry_id = entry_id
                        
                        else:
                            await connector.execute(
                                WAIFU_STATS_TABLE.update(
                                    waifu_stats_model.id == entry_id,
                                ).values(
                                    stat_housewife = self.stat_housewife,
                                    stat_cuteness = self.stat_cuteness,
                                    stat_bedroom = self.stat_bedroom,
                                    stat_charm = self.stat_charm,
                                    stat_loyalty = self.stat_loyalty,
                                    
                                    level = self.level,
                                    experience = self.experience,
                                    
                                    raw_species = self.raw_species,
                                    raw_weapon = self.raw_weapon,
                                    raw_costume = self.raw_costume,
                                )
                            )
                    
                        if self.saving_state == SAVING_STATE_RE_SAVE:
                            self.saving_state = SAVING_STATE_SAVING
                            continue
                        
                        break
            finally:
                self.saving_state = SAVING_STATE_NONE
    
    
    def __bool__(self):
        return self.entry_id not in (ENTRY_ID_NON_EXISTENT, ENTRY_ID_INITIALIZING)
    
    
    def __getstate__(self):
        state = {
            'user_id': self.user_id,
            'entry_id': self.entry_id,
            'stat_housewife': self.stat_housewife,
            'stat_cuteness': self.stat_cuteness,
            'stat_bedroom': self.stat_bedroom,
            'stat_charm': self.stat_charm,
            'stat_loyalty': self.stat_loyalty,
            'level': self.level,
            'experience': self.experience,
            'raw_species': self.raw_species,
            'raw_weapon': self.raw_weapon,
            'raw_costume': self.raw_costume,
        }
    
    
    def __setstate__(self, state):
        self.user_id = state['user_id']
        self.saving_state = SAVING_STATE_NONE
        self.entry_id = state['entry_id']
        self.stat_housewife = state['stat_housewife']
        self.stat_cuteness = state['stat_cuteness']
        self.stat_bedroom = state['stat_bedroom']
        self.stat_charm = state['stat_charm']
        self.stat_loyalty = state['stat_loyalty']
        self.level = state['level']
        self.experience = state['experience']
        self.raw_species = state['raw_species']
        self.raw_weapon = state['raw_weapon']
        self.raw_costume = state['raw_costume']
