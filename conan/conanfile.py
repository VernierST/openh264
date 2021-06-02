from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration

class VstudmConan(ConanFile):
    python_requires = "vst-conan-helper/0.8@vernierst+vst-libs/main"
    python_requires_extend = "vst-conan-helper.VstConanBase"

    name = "openh264"
    version = "2.1.0"
    url = "https://github.com/VernierST/openh264"
    description = "H.264 codec"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    exports_sources = "../*", "!../conan", "!../build", "!../*.bc", "!../*.a", "!../*.wasm"

    def init(self):
        base = self.python_requires["vst-conan-helper"].module.VstConanBase
        base.vst_setup(base, self)
        self.license = "MIT"

    def validate(self):
        if self.settings.os != "Emscripten":
            raise ConanInvalidConfiguration("Only emscripten build supported")

    def build(self):
        self.run(["emmake", "make", "PREFIX=\"%s\"" % (self.install_folder), "install"]);

    def package(self):
        self.copy("lib/*.bc", dst="lib", keep_path=False, symlinks=True)
        self.copy("lib/*.a", dst="lib", keep_path=False, symlinks=True)
        self.copy("include/wels/*", keep_path=True)

    def package_info(self):
        self.cpp_info.includedirs = ['include']
        self.cpp_info.libs = [ 'openh264']
        self.cpp_info.libdirs = ['lib']

    def package_id(self):
        self.vst_package_id()

    def build_id(self):
        self.vst_build_id()
