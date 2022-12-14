from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService
from Components.Element import cached
from os import path
WIDESCREEN = [
 1, 3, 4, 7, 8, 11, 12, 15, 16]

class qatServiceInfo(Converter, object):
    HAS_TELETEXT = 1
    IS_MULTICHANNEL = 2
    AUDIO_STEREO = 3
    IS_CRYPTED = 4
    IS_WIDESCREEN = 5
    IS_NOT_WIDESCREEN = 6
    SUBSERVICES_AVAILABLE = 7
    XRES = 8
    YRES = 9
    APID = 10
    VPID = 11
    PCRPID = 12
    PMTPID = 13
    TXTPID = 14
    TSID = 15
    ONID = 16
    SID = 17
    FRAMERATE = 18
    TRANSFERBPS = 19
    AUDIOTRACKS_AVAILABLE = 20
    SUBTITLES_AVAILABLE = 21
    EDITMODE = 22
    IS_STREAM = 23
    IS_SD = 24
    IS_HD = 25
    IS_1080 = 26
    IS_720 = 27
    IS_576 = 28
    IS_480 = 29
    IS_4K = 30
    IS_IPSTREAM = 31

    def __init__(self, type):
        Converter.__init__(self, type)
        self.type, self.interesting_events = {'HasTelext': (
                       self.HAS_TELETEXT, (iPlayableService.evUpdatedInfo,)),
           'IsMultichannel': (
                            self.IS_MULTICHANNEL, (iPlayableService.evUpdatedInfo,)),
           'IsStereo': (
                      self.AUDIO_STEREO, (iPlayableService.evUpdatedInfo,)),
           'IsCrypted': (
                       self.IS_CRYPTED, (iPlayableService.evUpdatedInfo,)),
           'IsWidescreen': (
                          self.IS_WIDESCREEN, (iPlayableService.evVideoSizeChanged,)),
           'IsNotWidescreen': (
                             self.IS_NOT_WIDESCREEN, (iPlayableService.evVideoSizeChanged,)),
           'SubservicesAvailable': (
                                  self.SUBSERVICES_AVAILABLE, (iPlayableService.evUpdatedEventInfo,)),
           'VideoWidth': (
                        self.XRES, (iPlayableService.evVideoSizeChanged,)),
           'VideoHeight': (
                         self.YRES, (iPlayableService.evVideoSizeChanged,)),
           'AudioPid': (
                      self.APID, (iPlayableService.evUpdatedInfo,)),
           'VideoPid': (
                      self.VPID, (iPlayableService.evUpdatedInfo,)),
           'PcrPid': (
                    self.PCRPID, (iPlayableService.evUpdatedInfo,)),
           'PmtPid': (
                    self.PMTPID, (iPlayableService.evUpdatedInfo,)),
           'TxtPid': (
                    self.TXTPID, (iPlayableService.evUpdatedInfo,)),
           'TsId': (
                  self.TSID, (iPlayableService.evUpdatedInfo,)),
           'OnId': (
                  self.ONID, (iPlayableService.evUpdatedInfo,)),
           'Sid': (
                 self.SID, (iPlayableService.evUpdatedInfo,)),
           'Framerate': (
                       self.FRAMERATE, (iPlayableService.evVideoSizeChanged, iPlayableService.evUpdatedInfo)),
           'TransferBPS': (
                         self.TRANSFERBPS, (iPlayableService.evUpdatedInfo,)),
           'AudioTracksAvailable': (
                                  self.AUDIOTRACKS_AVAILABLE, (iPlayableService.evUpdatedInfo,)),
           'SubtitlesAvailable': (
                                self.SUBTITLES_AVAILABLE, (iPlayableService.evUpdatedInfo,)),
           'Editmode': (
                      self.EDITMODE, (iPlayableService.evUpdatedInfo,)),
           'IsStream': (
                      self.IS_STREAM, (iPlayableService.evUpdatedInfo,)),
           'IsSD': (
                  self.IS_SD, (iPlayableService.evVideoSizeChanged,)),
           'IsHD': (
                  self.IS_HD, (iPlayableService.evVideoSizeChanged,)),
           'Is1080': (
                    self.IS_1080, (iPlayableService.evVideoSizeChanged,)),
           'Is720': (
                   self.IS_720, (iPlayableService.evVideoSizeChanged,)),
           'Is576': (
                   self.IS_576, (iPlayableService.evVideoSizeChanged,)),
           'Is480': (
                   self.IS_480, (iPlayableService.evVideoSizeChanged,)),
           'Is4K': (
                  self.IS_4K, (iPlayableService.evVideoSizeChanged,)),
           'IsIPStream': (
                        self.IS_IPSTREAM, (iPlayableService.evUpdatedInfo,))}[type]

    def getServiceInfoString(self, info, what, convert=lambda x: '%d' % x):
        v = info.getInfo(what)
        if v == -1:
            return 'N/A'
        if v == -2:
            return info.getInfoString(what)
        return convert(v)

    def getServiceInfoHexString(self, info, what, convert=lambda x: '%04x' % x):
        v = info.getInfo(what)
        if v == -1:
            return 'N/A'
        if v == -2:
            return info.getInfoString(what)
        return convert(v)

    @cached
    def getBoolean(self):
        service = self.source.service
        info = service and service.info()
        if not info:
            return False
        else:
            video_height = None
            video_width = None
            video_aspect = None
            if path.exists('/proc/stb/vmpeg/0/yres'):
                f = open('/proc/stb/vmpeg/0/yres', 'r')
                try:
                    video_height = int(f.read(), 16)
                except:
                    pass

                f.close()
            if path.exists('/proc/stb/vmpeg/0/xres'):
                f = open('/proc/stb/vmpeg/0/xres', 'r')
                try:
                    video_width = int(f.read(), 16)
                except:
                    pass

                f.close()
            if path.exists('/proc/stb/vmpeg/0/aspect'):
                f = open('/proc/stb/vmpeg/0/aspect', 'r')
                try:
                    video_aspect = int(f.read())
                except:
                    pass

                f.close()
            if not video_height:
                video_height = int(info.getInfo(iServiceInformation.sVideoHeight))
            if not video_aspect:
                video_aspect = info.getInfo(iServiceInformation.sAspect)
            if self.type == self.HAS_TELETEXT:
                tpid = info.getInfo(iServiceInformation.sTXTPID)
                return tpid != -1
            if self.type in (self.IS_MULTICHANNEL, self.AUDIO_STEREO):
                audio = service.audioTracks()
                if audio:
                    n = audio.getNumberOfTracks()
                    idx = 0
                    while idx < n:
                        i = audio.getTrackInfo(idx)
                        description = i.getDescription()
                        if description and description.split()[0] in ('AC3', 'AC-3',
                                                                      'AC3+', 'DTS'):
                            if self.type == self.IS_MULTICHANNEL:
                                return True
                            if self.type == self.AUDIO_STEREO:
                                return False
                        idx += 1

                    if self.type == self.IS_MULTICHANNEL:
                        return False
                    if self.type == self.AUDIO_STEREO:
                        return True
                return False
            if self.type == self.IS_CRYPTED:
                return info.getInfo(iServiceInformation.sIsCrypted) == 1
            if self.type == self.IS_WIDESCREEN:
                return video_aspect in WIDESCREEN
            if self.type == self.IS_NOT_WIDESCREEN:
                return video_aspect not in WIDESCREEN
            if self.type == self.SUBSERVICES_AVAILABLE:
                return hasActiveSubservicesForCurrentChannel((':').join(info.getInfoString(iServiceInformation.sServiceref).split(':')[:11]))
            if self.type == self.AUDIOTRACKS_AVAILABLE:
                audio = service.audioTracks()
                return audio and audio.getNumberOfTracks() > 1
            if self.type == self.SUBTITLES_AVAILABLE:
                try:
                    subtitle = service and service.subtitle()
                    subtitlelist = subtitle and subtitle.getSubtitleList()
                    if subtitlelist:
                        return len(subtitlelist) > 0
                    return False
                except:
                    try:
                        subtitle = service and service.subtitleTracks()
                        return subtitle and subtitle.getNumberOfSubtitleTracks() > 0
                    except:
                        return False

            else:
                if self.type == self.EDITMODE:
                    return hasattr(self.source, 'editmode') and not not self.source.editmode
                else:
                    if self.type == self.IS_STREAM:
                        return service.streamed() is not None
                    if self.type == self.IS_SD:
                        return video_height < 720
                    if self.type == self.IS_HD:
                        return video_height >= 720 and video_height < 2160
                    if self.type == self.IS_4K:
                        return video_height >= 2160 and video_height < 4320
                    if self.type == self.IS_1080:
                        return video_height >= 1080 and video_height <= 2119
                    if self.type == self.IS_720:
                        return video_height >= 720 and video_height <= 1019
                    if self.type == self.IS_576:
                        return video_height >= 576 and video_height <= 719
                    if self.type == self.IS_480:
                        return video_height > 0 and video_height <= 575
                    return False

            return

    boolean = property(getBoolean)

    @cached
    def getText(self):
        video_rate = 0
        service = self.source.service
        info = service and service.info()
        if not info:
            return ''
        else:
            if self.type == self.XRES:
                video_width = None
                if path.exists('/proc/stb/vmpeg/0/xres'):
                    f = open('/proc/stb/vmpeg/0/xres', 'r')
                    try:
                        video_width = int(f.read(), 16)
                    except:
                        pass

                    f.close()
                if not video_width:
                    try:
                        video_width = int(self.getServiceInfoString(info, iServiceInformation.sVideoWidth))
                    except:
                        return ''

                return '%d' % video_width
            if self.type == self.YRES:
                video_height = None
                if path.exists('/proc/stb/vmpeg/0/yres'):
                    f = open('/proc/stb/vmpeg/0/yres', 'r')
                    try:
                        video_height = int(f.read(), 16)
                    except:
                        pass

                    f.close()
                if not video_height:
                    try:
                        video_height = int(self.getServiceInfoString(info, iServiceInformation.sVideoHeight))
                    except:
                        return ''

                return '%d' % video_height
            if self.type == self.APID:
                return self.getServiceInfoString(info, iServiceInformation.sAudioPID)
            if self.type == self.VPID:
                return self.getServiceInfoString(info, iServiceInformation.sVideoPID)
            if self.type == self.PCRPID:
                return self.getServiceInfoString(info, iServiceInformation.sPCRPID)
            if self.type == self.PMTPID:
                return self.getServiceInfoString(info, iServiceInformation.sPMTPID)
            if self.type == self.TXTPID:
                return self.getServiceInfoString(info, iServiceInformation.sTXTPID)
            if self.type == self.TSID:
                return self.getServiceInfoString(info, iServiceInformation.sTSID)
            if self.type == self.ONID:
                return self.getServiceInfoString(info, iServiceInformation.sONID)
            if self.type == self.SID:
                return self.getServiceInfoHexString(info, iServiceInformation.sSID)
            if self.type == self.FRAMERATE:
                if path.exists('/proc/stb/vmpeg/0/framerate'):
                    f = open('/proc/stb/vmpeg/0/framerate', 'r')
                    try:
                        video_rate = int(f.read())
                    except:
                        pass

                    f.close()
                fps = str((video_rate + 500) / 1000)
                return str('fps') + fps
            if self.type == self.TRANSFERBPS:
                return self.getServiceInfoString(info, iServiceInformation.sTransferBPS, lambda x: '%d kB/s' % (x / 1024))
            return ''

    text = property(getText)

    @cached
    def getValue(self):
        video_rate = 0
        service = self.source.service
        info = service and service.info()
        if not info:
            return -1
        else:
            if self.type == self.XRES:
                video_width = None
                if path.exists('/proc/stb/vmpeg/0/xres'):
                    f = open('/proc/stb/vmpeg/0/xres', 'r')
                    try:
                        video_width = int(f.read(), 16)
                    except:
                        video_width = None

                    f.close()
                if not video_width:
                    video_width = info.getInfo(iServiceInformation.sVideoWidth)
                return str(video_width)
            if self.type == self.YRES:
                video_height = None
                if path.exists('/proc/stb/vmpeg/0/yres'):
                    f = open('/proc/stb/vmpeg/0/yres', 'r')
                    try:
                        video_height = int(f.read(), 16)
                    except:
                        video_height = None

                    f.close()
                if not video_height:
                    video_height = info.getInfo(iServiceInformation.sVideoHeight)
                return str(video_height)
            if self.type == self.FRAMERATE:
                if path.exists('/proc/stb/vmpeg/0/framerate'):
                    f = open('/proc/stb/vmpeg/0/framerate', 'r')
                    try:
                        video_rate = int(f.read())
                    except:
                        pass

                    f.close()
                fps = str((video_rate + 500) / 1000)
                return str('fps') + fps
            return -1

    value = property(getValue)

    def changed(self, what):
        if what[0] != self.CHANGED_SPECIFIC or what[1] in self.interesting_events:
            Converter.changed(self, what)
