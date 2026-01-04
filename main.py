from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import RoundedRectangle, Color
from kivy.properties import BooleanProperty
from kivy.core.text import LabelBase

# 注册中文字体（安卓安全加载）
try:
    LabelBase.register(name='SimHei', fn_regular='/system/fonts/DroidSansFallback.ttf')
except:
    try:
        LabelBase.register(name='SimHei', fn_regular='/system/fonts/NotoSansCJK-Regular.ttc')
    except:
        pass  # 安卓找不到字体就用默认字体

# 自定义胶囊按钮（高度生效+按下暗化）
class CapsuleButton(Button):
    is_pressed = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.color = get_color_from_hex('#000000')
        self.size_hint_y = None
        self.bind(height=lambda s, h: setattr(s, 'radius', [h / 2]))
        self.bind(pos=self.update_rect, size=self.update_rect, is_pressed=self.update_rect)
        self.radius = [self.height / 2] if self.height else [30]

    def update_rect(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            color_map = {
                "暂停": get_color_from_hex('#e74c3c'),
                "继续": get_color_from_hex('#2ecc71'),
                "设置": get_color_from_hex('#3498db'),
                "重置": get_color_from_hex('#95a5a6'),
                "+": get_color_from_hex('#27ae60'),
                "-": get_color_from_hex('#e67e22')
            }
            base_color = color_map.get(self.text, get_color_from_hex('#95a5a6'))
            r, g, b, a = base_color
            if self.is_pressed:
                r, g, b = r * 0.8, g * 0.8, b * 0.8
            Color(r, g, b, a)
            RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.is_pressed = True
            self.update_rect()
            return super().on_touch_down(touch)
        return False

    def on_touch_up(self, touch):
        self.is_pressed = False
        self.update_rect()
        return super().on_touch_up(touch)

# 主应用
class CountApp(App):
    count = 0
    loop_num = 0
    is_paused = False
    count_limit = 100
    warn_threshold = 3

    def build(self):
        Window.clearcolor = get_color_from_hex('#f0f0f0')
        main_layout = BoxLayout(orientation='vertical', spacing=40, padding=30)

        # 上限设置
        limit_layout = BoxLayout(spacing=15, size_hint=(1, None), height=80)
        limit_label = Label(
            text="计数上限:",
            font_name='SimHei',
            font_size='24sp',
            color=get_color_from_hex('#2c3e50'),
            size_hint=(0.2, 1),
            halign='right'
        )
        limit_label.bind(size=lambda s, sz: setattr(s, 'text_size', sz))
        self.limit_input = TextInput(
            text=str(self.count_limit),
            font_name='SimHei',
            font_size='24sp',
            input_filter='int',
            size_hint=(0.15, 1),
            halign='center',
            multiline=False,
            background_color=get_color_from_hex('#ffffff'),
            border=(10, 10, 10, 10)
        )
        self.limit_input.bind(focus=lambda s, f: s.select_all() if f else None)
        set_limit_btn = CapsuleButton(
            text="设置",
            font_name='SimHei',
            font_size='20sp',
            size_hint=(0.2, 1),
            height=60
        )
        set_limit_btn.bind(on_press=self.set_count_limit)
        limit_layout.add_widget(Label(size_hint=(0.15, 1)))
        limit_layout.add_widget(limit_label)
        limit_layout.add_widget(self.limit_input)
        limit_layout.add_widget(set_limit_btn)
        limit_layout.add_widget(Label(size_hint=(0.3, 1)))

        # 计数显示
        count_layout = BoxLayout(orientation='vertical', spacing=20, size_hint=(1, 0.5))
        self.count_label = Label(
            text=f"当前计数: {self.count} / {self.count_limit}",
            font_name='SimHei',
            font_size='45sp',
            color=get_color_from_hex('#2c3e50'),
            bold=True,
            halign='center',
            text_size=(Window.width * 0.9, None)
        )
        self.loop_label = Label(
            text=f"循环次数: {self.loop_num}",
            font_name='SimHei',
            font_size='28sp',
            color=get_color_from_hex('#7f8c8d'),
            halign='center'
        )
        self.count_label.bind(size=lambda s, sz: setattr(s, 'text_size', sz))
        self.loop_label.bind(size=lambda s, sz: setattr(s, 'text_size', sz))

        # 手动加减按钮
        count_ctrl_layout = BoxLayout(spacing=20, size_hint=(1, None), height=70)
        minus_btn = CapsuleButton(text="-", font_name='SimHei', font_size='24sp', size_hint=(0.1, 1), height=55)
        minus_btn.bind(on_press=self.minus_count)
        plus_btn = CapsuleButton(text="+", font_name='SimHei', font_size='24sp', size_hint=(0.1, 1), height=55)
        plus_btn.bind(on_press=self.plus_count)
        count_ctrl_layout.add_widget(Label(size_hint=(0.4, 1)))
        count_ctrl_layout.add_widget(minus_btn)
        count_ctrl_layout.add_widget(plus_btn)
        count_ctrl_layout.add_widget(Label(size_hint=(0.4, 1)))

        count_layout.add_widget(self.count_label)
        count_layout.add_widget(self.loop_label)
        count_layout.add_widget(count_ctrl_layout)

        # 功能按钮
        btn_layout = BoxLayout(spacing=25, size_hint=(1, None), height=90)
        self.pause_btn = CapsuleButton(text="暂停", font_name='SimHei', font_size='22sp', size_hint=(0.4, 1), height=70)
        self.pause_btn.bind(on_press=self.toggle_pause)
        reset_btn = CapsuleButton(text="重置", font_name='SimHei', font_size='22sp', size_hint=(0.4, 1), height=70)
        reset_btn.bind(on_press=self.reset_count)
        btn_layout.add_widget(Label(size_hint=(0.05, 1)))
        btn_layout.add_widget(self.pause_btn)
        btn_layout.add_widget(reset_btn)
        btn_layout.add_widget(Label(size_hint=(0.05, 1)))

        main_layout.add_widget(limit_layout)
        main_layout.add_widget(count_layout)
        main_layout.add_widget(btn_layout)

        Clock.schedule_interval(self.update_count, 1)
        return main_layout

    def minus_count(self, instance):
        self.count = self.count - 1 if self.count > 0 else self.count_limit - 1
        self.update_labels()

    def plus_count(self, instance):
        self.count += 1
        if self.count >= self.count_limit:
            self.count = 0
            self.loop_num += 1
        self.update_labels()

    def set_count_limit(self, instance):
        try:
            new_limit = int(self.limit_input.text)
            if new_limit > 0:
                self.count_limit = new_limit
                self.warn_threshold = max(1, int(self.count_limit * 0.1))
                self.update_labels()
        except ValueError:
            self.limit_input.text = str(self.count_limit)

    def update_count_color(self):
        remaining = self.count_limit - self.count
        self.count_label.color = get_color_from_hex('#e74c3c') if 0 < remaining <= self.warn_threshold else get_color_from_hex('#2c3e50')

    def update_labels(self):
        self.count_label.text = f"当前计数: {self.count} / {self.count_limit}"
        self.loop_label.text = f"循环次数: {self.loop_num}"
        self.update_count_color()

    def update_count(self, dt):
        if self.is_paused:
            return
        self.count += 1
        if self.count >= self.count_limit:
            self.count = 0
            self.loop_num += 1
        self.update_labels()

    def toggle_pause(self, instance):
        self.is_paused = not self.is_paused
        self.pause_btn.text = "继续" if self.is_paused else "暂停"
        self.pause_btn.update_rect()  # 刷新颜色

    def reset_count(self, instance):
        self.count = 0
        self.loop_num = 0
        self.update_labels()

if __name__ == "__main__":
    CountApp().run()