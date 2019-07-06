import numpy
import logging


log = logging.getLogger(__name__)


class Notifications:
    CHECK_LOOP_MS = 500
    TOTALTIME_MS = 20000

    def __init__(self):
        self.actual_cnt = 0
        self.max_cnt = Notifications.TOTALTIME_MS / Notifications.CHECK_LOOP_MS
        self.alert_color = (255, 255, 36)
        self.base_color = (255, 255, 255)
        log.info('Notification class initiated')

    def new_notification_color(self):
        self.actual_cnt = Notifications.TOTALTIME_MS / Notifications.CHECK_LOOP_MS
        log.info('New notification')
        return self.alert_color

    def new_color(self, actual_color):
        actual_color = Notifications.hex_to_rgb(actual_color)
        if self.actual_cnt > 0:
            ramping = self._eval_ramp(actual_color, self.base_color, self.actual_cnt)
            new_color = numpy.subtract(actual_color, ramping)
            new_color = numpy.uint8(new_color)
            new_color = tuple(new_color)
            self.actual_cnt -= 1
        else:
            new_color = actual_color
        # log.info('new color {}'.format(new_color))
        return new_color

    def _eval_ramp(self, first_color, second_color, count):
        log.info('first: {} second: {}'.format(first_color, second_color))
        diff_color = numpy.subtract(first_color, second_color)
        ramp_color = numpy.divide(diff_color, count)
        ramp_color = numpy.int16(ramp_color)
        log.info('eval ramp at {}'.format(ramp_color))
        return ramp_color

    @staticmethod
    def hex_to_rgb(value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + int(lv / 3)], 16) for i in range(0, lv, int(lv / 3)))
