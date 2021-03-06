export * from './admin.service';
import { AdminService } from './admin.service';
export * from './badwords.service';
import { BadwordsService } from './badwords.service';
export * from './email.service';
import { EmailService } from './email.service';
export * from './hoods.service';
import { HoodsService } from './hoods.service';
export * from './telegram.service';
import { TelegramService } from './telegram.service';
export * from './test.service';
import { TestService } from './test.service';
export * from './triggers.service';
import { TriggersService } from './triggers.service';
export * from './twitter.service';
import { TwitterService } from './twitter.service';
export const APIS = [AdminService, BadwordsService, EmailService, HoodsService, TelegramService, TestService, TriggersService, TwitterService];
