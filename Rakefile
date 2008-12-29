include FileUtils
GEDIT = File.join ENV['HOME'], '.gnome2/gedit/'

namespace :install do
  desc 'installs snippets, plugins and styles locally'
  task :local do
    mkdir_p GEDIT
    %w(plugins snippets styles).each do |dir|
      cp_r dir, GEDIT
    end
  end
  
  desc 'installs lang-specs, mime types and \'g\', command needs root priviliges'
  task :global do
    cp 'mime/rails.xml', '/usr/share/mime/packages/'
    %w(rhtml.lang ruby.lang yml.lang).each do |file|
      cp 'lang-specs/' + file, '/usr/share/gtksourceview-2.0/language-specs/'
    end
    cp 'bin/g', '/usr/bin/g'
    print `update-mime-database /usr/share/mime`
  end    
end

