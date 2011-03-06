if RUBY_VERSION < "1.9"
  require 'ftools'
else
  require 'fileutils'
end

include FileUtils
GEDIT = File.join ENV['HOME'], '.gnome2/gedit/'

namespace :install do
  desc 'install snippets, plugins and styles locally'
  task :local do
    mkdir_p GEDIT
    %w(plugins snippets styles).each do |dir|
      cp_r dir, GEDIT
    end
  end

  desc 'install lang-specs, mime types and \'g\', command needs root priviliges'
  task :global do
    Dir.glob("mime/*.xml") do |file|
        # Copy all files except rst.xml, it doesn't seem to be valid.
        cp file, '/usr/share/mime/packages/' unless file == 'mime/rst.xml'
    end
    Dir.glob("lang-specs/*.lang") do |file|
        cp file, '/usr/share/gtksourceview-2.0/language-specs/'
    end
    cp 'bin/g', '/usr/bin/g'
    chmod 0755, '/usr/bin/g', :verbose => true
    print `update-mime-database /usr/share/mime`
  end
end

