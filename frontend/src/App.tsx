import { Box, Flex, Stack } from '@chakra-ui/react';

import { SidebarProvider } from './sidebar-context';

import { Sidebar } from './sidebar';
import { TopSection } from './top-section';
import { MiddleSection } from './middle-section';
import { BottomSection } from './bottom-section';

function App() {
  return (
    <SidebarProvider>
      <Flex minH="100vh">
        <Sidebar />

        <Box flex={1}>
          <Stack h="full">
            <TopSection />

            <MiddleSection />

            <BottomSection />
          </Stack>
        </Box>
      </Flex>
    </SidebarProvider>
  );
}

export default App;
