#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/team_beta/Rins/src/Turtlebot_packs_part2/yujin_ocs/yocs_localization_manager"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/team_beta/Rins/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/team_beta/Rins/install/lib/python3/dist-packages:/home/team_beta/Rins/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/team_beta/Rins/build" \
    "/usr/bin/python3" \
    "/home/team_beta/Rins/src/Turtlebot_packs_part2/yujin_ocs/yocs_localization_manager/setup.py" \
     \
    build --build-base "/home/team_beta/Rins/build/Turtlebot_packs_part2/yujin_ocs/yocs_localization_manager" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/team_beta/Rins/install" --install-scripts="/home/team_beta/Rins/install/bin"
