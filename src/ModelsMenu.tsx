import { Box, Circle, HStack, Stack, Text } from '@chakra-ui/react';
import { Button } from '@/components/ui/button';
import {
  MenuContent,
  MenuItem,
  MenuRoot,
  MenuSeparator,
  MenuTrigger,
} from '@/components/ui/menu';
import { Switch } from '@/components/ui/switch';

import {
  ChatGPTMenuIcon,
  ChatGPTPlusIcon,
  MenuIcon,
  TemporaryChatIcon,
} from './icons/other-icons';
import { FaCheckCircle } from 'react-icons/fa';

interface MenuItemDetailProps {
  icon: React.ReactElement;
  title: string;
  description?: string;
  element: React.ReactElement;
}

function MenuItemDetail(props: MenuItemDetailProps) {
  const { icon, title, description, element, ...rest } = props;
  return (
    <HStack w="100%" {...rest}>
      <Circle size={8} bg="bg.muted">
        {icon}
      </Circle>
      <Stack gap={0} flex={1}>
        <Text>{title}</Text>
        <Text fontSize="xs" color="fg.muted">
          {description}
        </Text>
      </Stack>
      <Box>{element}</Box>
    </HStack>
  );
}

export const ModelsMenu = () => {
  return (
    <MenuRoot>
      <MenuTrigger asChild>
        <Button variant="ghost" size="lg" fontWeight="bold" color="fb.muted">
          Models Prompt <MenuIcon />
        </Button>
      </MenuTrigger>

      <MenuContent minW="320px" borderRadius="2xl">
        <MenuItem value="mistral-model" py={2}>
          <MenuItemDetail
            title="Mistral Model"
            icon={<ChatGPTPlusIcon />}
            description="Other smartest model & more"
            element={
              <Button variant="outline" size="xs" borderRadius="full">
                Change
              </Button>
            }
          />
        </MenuItem>

        <MenuItem value="dall-e-model" py={2}>
          <MenuItemDetail
            title="Dall-E Model"
            icon={<ChatGPTMenuIcon />}
            description="Great for everyday tasks"
            element={<FaCheckCircle fontSize="lg" />}
          />
        </MenuItem>

        <MenuSeparator />

        <MenuItem value="temporary-prompts" py={2}>
          <MenuItemDetail
            title="Temporary prompts"
            icon={<TemporaryChatIcon />}
            element={<Switch size="sm" />}
          />
        </MenuItem>
      </MenuContent>
    </MenuRoot>
  );
};
