import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import MenuItem from '@mui/material/MenuItem';
import AdbIcon from '@mui/icons-material/Adb';
import { Link } from "react-router-dom";
import { useSelector, useDispatch } from 'react-redux';
import { logout } from '@/features/auth';


function handleProfileRequest() {

}

function handleAccountRequest() {

}

function handleSettingsRequest() {
  
}


export const NavBar = () => {
  const [anchorElNav, setAnchorElNav] = React.useState(null);
  const [anchorElUser, setAnchorElUser] = React.useState(null);

  const dispatch = useDispatch();
  const { isAuthenticated, user } = useSelector(state => state.user);


  // Avatar drop-down right side of navbar
  // If logged in
  const authMenu = [
      <MenuItem key="Profile" onClick={handleProfileRequest}>
        <Typography>Profile</Typography>
      </MenuItem>,
      <MenuItem key="Account" onClick={handleAccountRequest}>
        <Typography>Account</Typography>
      </MenuItem>,
      <MenuItem key="Settings" onClick={handleSettingsRequest}>
        <Typography>Settings</Typography>
      </MenuItem>,
      <MenuItem key="Logout" onClick={() => dispatch(logout())}>
        <Typography>Logout</Typography>
      </MenuItem>
  ];

  // If not logged in
  const guestMenu = [
    <MenuItem key='Register' component={Link} to="/register">
      <Typography>Register</Typography>
    </MenuItem>,
    <MenuItem key='Login' component={Link} to="/login">
      <Typography>Login</Typography>
    </MenuItem>
  ];

  // Navigation buttons on left side of navbar
  // Logged in
  const authPages = [
    <Button
      key='My Collections'
      component={Link}
      to={`/u/${user.username}/collections`}
      sx={{ my: 2, color: 'white', display: 'block', textTransform: 'capitalize'}}
    >
      My Collections
    </Button>
  ];

  // Not logged in
  const guestPages = [

  ];

  const handleOpenNavMenu = (event) => {
    setAnchorElNav(event.currentTarget);
  };
  
  const handleOpenUserMenu = (event) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  return (
    <AppBar position="static">
      <Container maxWidth='md' disableGutters>
        <Toolbar>
          <AdbIcon sx={{ display: { xs: 'none', md: 'flex' }, mr: 1 }} />
          <Typography
            variant="h6"
            noWrap
            component={Link}
            to="/"
            sx={{
              mr: 2,
              display: { xs: 'none', md: 'flex' },
              fontFamily: 'monospace',
              fontWeight: 700,
              color: 'inherit',
              textDecoration: 'none',
            }}
          >
            TFTracker
          </Typography>

          <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
            <IconButton
              size="large"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleOpenNavMenu}
              color="inherit"
            >
              <MenuIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorElNav}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'left',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'left',
              }}
              open={Boolean(anchorElNav)}
              onClose={handleCloseNavMenu}
              sx={{
                display: { xs: 'block', md: 'none' },
              }}
            >
              {isAuthenticated ? authPages : guestPages}
            </Menu>
          </Box>
          <AdbIcon sx={{ display: { xs: 'flex', md: 'none' }, mr: 1 }} />
          <Typography
            variant="h5"
            noWrap
            component="a"
            href=""
            sx={{
              mr: 2,
              display: { xs: 'flex', md: 'none' },
              flexGrow: 1,
              fontFamily: 'monospace',
              fontWeight: 700,
              color: 'inherit',
              textDecoration: 'none',
            }}
          >
            TFTracker
          </Typography>
          <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
            {user ? authPages : guestPages}
          </Box>

          <Box sx={{ flexGrow: 0, mr: 1 }}>
            <Tooltip title="Open settings">
              <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                <Avatar alt="Avatar" src="" />
              </IconButton>
            </Tooltip>
            <Menu
              sx={{ mt: '45px' }}
              id="menu-appbar"
              anchorEl={anchorElUser}
              anchorOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              open={Boolean(anchorElUser)}
              onClose={handleCloseUserMenu}
            >
            {isAuthenticated ? authMenu : guestMenu}
            
            </Menu>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
}