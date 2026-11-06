Name:		apache-commons-digester
Version:	2.1
Release:	1
Summary:	XML to Java object mapping
Group:		Development/Java
License:	ASL 2.0
URL:		https://commons.apache.org/proper/commons-digester/
Source0:	https://archive.apache.org/dist/commons/digester/source/commons-digester-%{version}-src.tar.gz

BuildArch:	noarch
Provides:	jakarta-commons-digester = %{version}-%{release}
Obsoletes:	jakarta-commons-digester < %{version}-%{release}
Obsoletes:	%{name}-javadoc < %{version}
BuildRequires:	python
BuildRequires:	mvn(org.apache.commons:commons-parent:pom::)
BuildRequires:	mvn(org.apache:apache:pom::)
BuildRequires:	mvn(commons-beanutils:commons-beanutils)
BuildRequires:	mvn(commons-logging:commons-logging)
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name commons-digester --link %{name}

%description
Apache Commons Digester maps nested XML elements to Java objects.
2.1 is the last release on the commons-digester coordinate. It needs
beanutils and commons-logging. Tests are skipped.

%prep
%autosetup -n commons-digester-%{version}-src
# The POM still names the pre-compiler-plugin-3 properties. 1.5 is
# rejected by the current JDK when something expands them.
python - <<'PY'
from pathlib import Path
path = Path("pom.xml")
text = path.read_text()
old = """    <maven.compile.source>1.5</maven.compile.source>
    <maven.compile.target>1.5</maven.compile.target>"""
new = """    <maven.compile.source>8</maven.compile.source>
    <maven.compile.target>8</maven.compile.target>"""
if old not in text:
    raise SystemExit("compiler properties not found")
path.write_text(text.replace(old, new, 1))
PY

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt
